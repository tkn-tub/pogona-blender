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


def get_operator_for_object(object_definition: dict):
    """
    Create a Blender Operator for the given object definition.
    This Operator will allow adding the respective object to the scene.

    :param object_definition: dict defining a unique ID
        (across all of Blender), a name for the UI,
        a representation Blender (which ideally closely resembles the
        object's form in simulation), …
    :return:
    """
    class MetaAddObject(bpy.types.Operator):
        """

        """
        bl_idname = object_definition.get('id')
        bl_label = object_definition.get('label')
        bl_options = {'REGISTER', 'UNDO'}
        # TODO?

        def execute(self, context) -> typing.Set[int]:
            pass  # TODO

    return MetaAddObject


def mamoko_type_update_callback(self, context):
    """For AddBoxObject.mamoko_type: Toggle the 'custom type' property"""
    self.mamoko_type_custom.active = self.mamoko_type == 'CUSTOM'
    # TODO: neither 'active' nor 'enabled' seems to work…


class AddBoxObject(bpy.types.Operator):
    mamoko_shape = 'cube'
    bl_idname = f'mamoko.add_cube'
    bl_label = "Add MaMoKo Cube Object"
    bl_options = {'REGISTER', 'UNDO'}

    type_items_default = (
        ('INJECTOR', "Injector", "A generic MaMoKo injector"),
        ('SENSOR', "Sensor", "A generic MaMoKo sensor"),
        ('CUSTOM', "Custom", "Specify the class name yourself"),
    )
    mamoko_type: EnumProperty(
        name="Type",
        items=type_items_default,
        default='CUSTOM',
        update=mamoko_type_update_callback
    )
    mamoko_type_custom: StringProperty(
        name="Custom Type",
        default=""
    )

    # generic transform props
    # align_items = (
    #     ('WORLD', "World", "Align the new object to the world"),
    #     ('VIEW', "View", "Align the new object to the view"),
    #     ('CURSOR', "3D Cursor",
    #      "Use the 3D cursor orientation for the new object")
    # )
    # align: EnumProperty(
    #     name="Align",
    #     items=align_items,
    #     default='WORLD',
    #     update=AddObjectHelper.align_update_callback,
    # )
    # location: FloatVectorProperty(
    #     name="Location",
    #     subtype='TRANSLATION',
    # )
    # rotation: FloatVectorProperty(
    #     name="Rotation",
    #     subtype='EULER',
    # )
    # scale: FloatVectorProperty(
    #     name="Scale",
    #     subtype='DIRECTION'
    # )

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
        obj = bpy.context.active_object
        obj['mamoko_type'] = (
            self.mamoko_type
            if self.mamoko_type != 'CUSTOM'
            else self.mamoko_type_custom
        )
        obj['mamoko_shape'] = self.mamoko_shape

        return {'FINISHED'}
