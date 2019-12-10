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

        if not obj.get('mamoko_molecule_visualization_flag', False):
            continue
        if (
                obj_eval.mamoko_molecule_positions_step == obj_eval.get(
                    '_mamoko_molecule_position_previous_step'
                )
                and not obj_eval.get(
                    '_mamoko_molecule_position_force_update',
                    True
                )
        ):
            # Don't update if the object's time step hasn't changed.
            print(f"time step of {obj.name} hasn't changed; "
                  f"old: "
                  f"{obj_eval.get('_mamoko_molecule_position_previous_step')},"
                  f" new: {obj_eval.mamoko_molecule_positions_step}, "
                  f"force update: "
                  f"{obj_eval.get('_mamoko_molecule_position_force_update')}")
            continue
        print(
            f"Updating molecule visualizations, frame {scene.frame_current}, "
            f"object '{obj.name}'."
        )

        mesh = bpy.data.meshes.new(obj.name)
        verts = []
        scale = 1 / scene.unit_settings.scale_length
        filename = bpy.path.abspath(os.path.join(
            obj.mamoko_molecule_positions_path,
            f'positions.csv.{obj_eval.mamoko_molecule_positions_step}'
        ))
        try:
            with open(filename, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    verts.append(mathutils.Vector((
                        float(row['x']) * scale,
                        float(row['y']) * scale,
                        float(row['z']) * scale
                    )))
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

        obj['_mamoko_molecule_position_previous_step'] = (
            obj_eval.mamoko_molecule_positions_step)
        obj['_mamoko_molecule_position_force_update'] = False


@persistent
def _lock_ui_during_render(scene):
    """
    If this is omitted, Blender may segfault when rendering animations
    with this add-on enabled.
    As @dr.sybren on blender.chat pointed out:
    This needs the viewport to be locked while rendering,
    to avoid multi-threading issues.

    This function is equivalent to checking Render -> Lock Interface.
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
