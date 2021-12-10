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
import bmesh
import mathutils
import bpy_extras


def _undo_unit_scale(context, bm):
    scale = 1 / context.scene.unit_settings.scale_length
    bmesh.ops.scale(
        bm,
        vec=mathutils.Vector((scale, scale, scale)),
        space=mathutils.Matrix.Identity(4),
        verts=bm.verts
    )


def _create_cube_mesh(context, mesh, bm):
    _ = bmesh.ops.create_cube(
        bm,
        size=1,
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    _undo_unit_scale(context, bm)
    bm.to_mesh(mesh)
    mesh.update()


def _create_cylinder_mesh(context, mesh, bm):
    _ = bmesh.ops.create_cone(
        bm,
        cap_ends=True,  # close ends
        segments=32,
        radius1=0.5,
        radius2=0.5,
        depth=1,
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    _undo_unit_scale(context, bm)
    bm.to_mesh(mesh)
    mesh.update()


def _create_sphere_mesh(context, mesh, bm):
    _ = bmesh.ops.create_uvsphere(
        bm,
        u_segments=32,
        v_segments=32,
        diameter=0.5,  # actually radius, apparently
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    _undo_unit_scale(context, bm)
    bm.to_mesh(mesh)
    mesh.update()


def _create_cross_mesh(context, mesh, bm):
    size = 0.5 / context.scene.unit_settings.scale_length
    verts = [
        mathutils.Vector((-size, 0, 0)),
        mathutils.Vector((size, 0, 0)),
        mathutils.Vector((0, -size, 0)),
        mathutils.Vector((0, size, 0)),
        mathutils.Vector((0, 0, -size)),
        mathutils.Vector((0, 0, size))
    ]
    edges = [
        (0, 1),
        (2, 3),
        (4, 5)
    ]
    mesh.from_pydata(verts, edges, [])


def _create_pogona_object(self, context, create_mesh_func):
    mesh = bpy.data.meshes.new(f"Pogona {self.bl_label}")
    bm = bmesh.new()
    create_mesh_func(context, mesh, bm)
    bpy_extras.object_utils.object_data_add(context, mesh, operator=None)

    obj = context.active_object

    # Mark this object as part of the Pogona scene
    # (important for exporting and for toggling UI):
    obj['pogona_flag'] = True

    # Apply scene unit scale to the object (not the mesh).
    # If you're working on a millimeter scale, for example,
    # this will scale down the 1 m objects to 1 mm in a way
    # that preserves your ability to set the scale in meters.
    scale = context.scene.unit_settings.scale_length
    obj.scale = [scale, scale, scale]

    return {'FINISHED'}


class PogonaRepresentationShapeUpdate(bpy.types.Operator):
    bl_idname = 'pogona.update_representation_shape'
    bl_label = "Update Representation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if (obj.pogona_representation.same_as_shape
                or obj.pogona_representation.linked_object is None):
            mesh = bpy.data.meshes.new(obj.name)
            bm = bmesh.new()
            if obj.pogona_shape == 'CUBE':
                _create_cube_mesh(context, mesh, bm)
            elif obj.pogona_shape == 'CYLINDER':
                _create_cylinder_mesh(context, mesh, bm)
            elif obj.pogona_shape == 'SPHERE':
                _create_sphere_mesh(context, mesh, bm)
            else:
                # obj.pogona_shape in ('POINT', 'NONE'):
                _create_cross_mesh(context, mesh, bm)
            obj.data = mesh
        else:
            obj.data = obj.pogona_representation.linked_object.data

        return {'FINISHED'}


class PogonaRepresentationScaleUpdate(bpy.types.Operator):
    """
    Update the scale in Blender based on the Pogona component scale and
    the additional visualization scale.
    """
    bl_idname = 'pogona.update_representation_scale'
    bl_label = "Update scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        unit_scale = context.scene.unit_settings.scale_length
        new_scale = [
            obj.pogona_component_scale[i]
            * unit_scale  # component_scale is defined as LENGTH
            * obj.pogona_representation.additional_scale[i]  # this is not
            for i in range(3)
        ]
        obj.scale = new_scale
        return {'FINISHED'}


class PogonaAddCube(bpy.types.Operator):
    """A cube with origin at the center."""
    bl_idname = 'pogona.add_cube'
    bl_label = "Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_pogona_object(self, context, _create_cube_mesh)
        obj = context.active_object
        obj.pogona_shape = 'CUBE'
        return {'FINISHED'}


class PogonaAddCylinder(bpy.types.Operator):
    """A cylinder with origin at the center."""
    bl_idname = 'pogona.add_cylinder'
    bl_label = "Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_pogona_object(self, context, _create_cylinder_mesh)
        obj = context.active_object
        obj.pogona_shape = 'CYLINDER'
        return {'FINISHED'}


class PogonaAddSphere(bpy.types.Operator):
    """A sphere with origin at the center."""
    bl_idname = 'pogona.add_sphere'
    bl_label = "Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_pogona_object(self, context, _create_sphere_mesh)
        obj = context.active_object
        obj.pogona_shape = 'SPHERE'
        return {'FINISHED'}


class PogonaAddPoint(bpy.types.Operator):
    """A simple point shape."""
    bl_idname = 'pogona.add_point'
    bl_label = "Point"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_pogona_object(self, context, _create_cross_mesh)
        obj = context.active_object
        obj.pogona_shape = 'POINT'
        return {'FINISHED'}


class PogonaAddMoleculesVisualization(bpy.types.Operator):
    """Periodically load molecule position CSVs for visualization"""
    bl_idname = 'pogona.add_moleculesvis'
    bl_label = "Molecules Visualization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Not using _create_pogona_object,
        # as this is just for visualization and is not supposed to be
        # exportable to be used in the Pogona simulator.
        mesh = bpy.data.meshes.new(f"Pogona {self.bl_label}")
        bm = bmesh.new()
        # Create initial placeholder mesh.
        # The actual mesh will be vertices loaded from CSVs for every frame.
        _create_cross_mesh(context, mesh, bm)
        bpy_extras.object_utils.object_data_add(context, mesh, operator=None)

        obj = context.active_object

        # Mark this object so we can later check whether to enable
        # relevant UI elements or not:
        obj['pogona_molecule_visualization_flag'] = True

        return {'FINISHED'}
