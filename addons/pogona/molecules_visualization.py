# Pogona Blender add-on
# Copyright (C) 2020 Data Communications and Networking (TKN), TU Berlin
#
# This file is part of Pogona, a simulator for macroscopic molecular
# communication.
#
# Pogona is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pogona is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pogona.  If not, see <https://www.gnu.org/licenses/>.import bpy

import bpy
import mathutils
from bpy.app.handlers import persistent
import os
import csv
from . import util


@persistent
def _update_all_molecule_visualizations(scene, depsgraph):
    for obj in scene.objects:
        # When rendering, it can happen that key-framed properties
        # are not updated in the 'original datablock',
        # hence we need to get the 'evaluated version'
        # (see https://developer.blender.org/T63548):
        obj_eval = obj.evaluated_get(depsgraph)
        # TODO: this requires frame_change_post, does not work with …pre.
        #  Does this mean we're one frame off?

        if not obj.get('pogona_molecule_visualization_flag', False):
            continue
        if (
                obj_eval.pogona_molecule_positions_step == obj_eval.get(
                    '_pogona_molecule_position_previous_step'
                )
                and not obj_eval.get(
                    '_pogona_molecule_position_force_update',
                    True
                )
        ):
            # Don't update if the object's time step hasn't changed.
            print(f"time step of {obj.name} hasn't changed; "
                  f"old: "
                  f"{obj_eval.get('_pogona_molecule_position_previous_step')},"
                  f" new: {obj_eval.pogona_molecule_positions_step}, "
                  f"force update: "
                  f"{obj_eval.get('_pogona_molecule_position_force_update')}")
            continue
        print(
            f"Updating molecule visualizations, frame {scene.frame_current}, "
            f"object '{obj.name}'."
        )

        mesh = bpy.data.meshes.new(obj.name)
        verts = []

        # Data for Geometry Nodes attributes:
        attr_data = {
            item.pogona_particle_attr: []
            for item in obj.pogona_molecule_attributes
        }
        attr_type_by_name = {
            item.pogona_particle_attr: item.pogona_particle_attr_type
            for item in obj.pogona_molecule_attributes
        }

        scale = 1 / scene.unit_settings.scale_length
        filename = bpy.path.abspath(os.path.join(
            obj.pogona_molecule_positions_path,
            f'positions.csv.{obj_eval.pogona_molecule_positions_step}'
        ))
        # bpy.path.abspath may still produce paths like
        # `/home/user/path/to/blendfile/../../../selected.file`
        # Can be resolved with os.path.abspath:
        filename = os.path.abspath(filename)
        try:
            with open(filename, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    verts.append(mathutils.Vector((
                        float(row['x']) * scale,
                        float(row['y']) * scale,
                        float(row['z']) * scale
                    )))

                    for attr_name, attr_type in attr_type_by_name.items():
                        if attr_name not in row:
                            raise ValueError(
                                f"Particle positions file {filename} "
                                f"has no column(s) for {attr_name}."
                            )
                        if attr_type == 'INT':
                            attr_data[attr_name].append(
                                int(row[attr_name])
                            )
                        elif attr_type == 'FLOAT':
                            attr_data[attr_name].append(
                                float(row[attr_name])
                            )
                        elif attr_type == 'STRING':
                            attr_data[attr_name].append(row[attr_name])
                        elif attr_type == 'STRING_HASH':
                            attr_data[attr_name].append(
                                hash(row[attr_name])
                            )
                        elif attr_type == 'FLOAT_VECTOR':
                            vec = (
                                float(row[attr_name + '_x']),
                                float(row[attr_name + '_y']),
                                float(row[attr_name + '_z']),
                            )
                            attr_data[attr_name].append(vec)

        except OSError as e:
            raise Warning(
                f"Could not open file '{filename}'. "
                "Skipping molecule positions update. "
                f"Exception: {e}"
            )
        mesh.from_pydata(verts, [], [])
        old_mesh = obj.data
        # Transfer the first material to the new mesh:
        if len(old_mesh.materials) > 0:
            tmp_material = old_mesh.materials[0]
            mesh.materials.append(tmp_material)

        mesh.update()
        obj.data = mesh
        util.delete_mesh(old_mesh)

        for attr_name, attr_type in attr_type_by_name.items():
            obj.data.attributes.new(
                name=attr_name,
                type=attr_type if attr_type != 'STRING_HASH' else 'INT',
                domain='POINT'
            )
            obj.data.attributes[attr_name].data.foreach_set(
                'vector' if attr_type == 'FLOAT_VECTOR' else 'value',
                attr_data[attr_name],
            )

        obj['_pogona_molecule_position_previous_step'] = (
            obj_eval.pogona_molecule_positions_step)
        obj['_pogona_molecule_position_force_update'] = False


@persistent
def _lock_ui_during_render(scene):
    """
    If this is omitted, Blender may segfault when rendering animations
    with this add-on enabled.
    As @dr.sybren on blender.chat pointed out:
    This needs the viewport to be locked while rendering,
    to avoid multi-threading issues.

    This function is equivalent to checking Render -> Lock Interface.
    # TODO: still necessary after that one bug fix?
    """
    bpy.context.scene.render.use_lock_interface = True


def register_handlers():
    bpy.app.handlers.frame_change_post.append(
        _update_all_molecule_visualizations
    )
    bpy.app.handlers.render_pre.append(_lock_ui_during_render)
    # Keep in mind that render_pre is run before every frame when
    # rendering an animation.


def unregister_handlers():
    bpy.app.handlers.frame_change_post.remove(
        _update_all_molecule_visualizations
    )
    bpy.app.handlers.render_pre.remove(_lock_ui_during_render)
