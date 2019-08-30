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


def mamoko_type_update_callback(self, context):
    """For AddBoxObject.mamoko_type: Toggle the 'custom type' property"""
    # help(self.mamoko_type)
    # self.mamoko_type_custom.active = self.mamoko_type == 'CUSTOM'
    # TODO: neither 'active' nor 'enabled' seems to work…
    # Not sure disabling properties on the fly is possible at all…


type_items_default = (
    ('INJECTOR', "Injector", "A generic MaMoKo injector"),
    ('SENSOR', "Sensor", "A generic MaMoKo sensor"),
    ('CUSTOM', "Custom", "Specify the class name yourself"),
)
mamoko_type_property = EnumProperty(
    name="Type",
    items=type_items_default,
    default='CUSTOM',
    update=mamoko_type_update_callback
)
mamoko_custom_type_property = StringProperty(
    name="Custom Type",
    default=""
)


def execute_common_mamoko_object_add(self, context) -> typing.Set:
    # Add common custom properties for MaMoKoExporter:
    obj = bpy.context.active_object
    obj['mamoko_type'] = (
        self.mamoko_type
        if self.mamoko_type != 'CUSTOM'
        else self.mamoko_type_custom
    )
    obj['mamoko_shape'] = self.mamoko_shape

    return {'FINISHED'}


class AddCubeObject(bpy.types.Operator):
    mamoko_shape = 'cube'
    bl_idname = f'mamoko.add_cube'
    bl_label = "Cube"
    bl_options = {'REGISTER', 'UNDO'}

    mamoko_type: mamoko_type_property
    mamoko_type_custom: mamoko_custom_type_property

    def execute(self, context) -> typing.Set:
        # verts, faces = add_box(self.width, self.height, self.length)

        mesh = bpy.data.meshes.new("MaMoKo Cube")
        bm = bmesh.new()
        verts_dict = bmesh.ops.create_cube(
            bm,
            size=1,
            matrix=mathutils.Matrix.Identity(4),
            calc_uvs=True
        )

        bm.to_mesh(mesh)
        mesh.update()

        object_data_add(context, mesh, operator=None)

        return execute_common_mamoko_object_add(self, context)
