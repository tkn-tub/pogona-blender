import bpy
from bpy.props import (
    EnumProperty,
    StringProperty,
    FloatVectorProperty,
)
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import bmesh
import mathutils
import typing


def execute_common_mamoko_object_add(self, context) -> typing.Set:
    # Add common custom properties for MaMoKoExporter:
    obj = bpy.context.active_object

    # Mark this object as part of the MaMoKo scene
    obj['mamoko_flag'] = True

    return {'FINISHED'}


class AddCubeObject(bpy.types.Operator):
    mamoko_shape = 'cube'
    bl_idname = f'mamoko.add_cube'
    bl_label = "Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context) -> typing.Set:
        # verts, faces = add_box(self.width, self.height, self.length)

        mesh = bpy.data.meshes.new("MaMoKo Cube")
        bm = bmesh.new()
        _ = bmesh.ops.create_cube(
            bm,
            size=1,
            matrix=mathutils.Matrix.Identity(4),
            calc_uvs=True
        )

        bm.to_mesh(mesh)
        mesh.update()

        object_data_add(context, mesh, operator=None)

        return execute_common_mamoko_object_add(self, context)
