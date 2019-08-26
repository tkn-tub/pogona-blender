import bpy
from bpy.props import (
    FloatProperty,
    EnumProperty,
    FloatVectorProperty,
)
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import bmesh
import mathutils
import typing

from .mesh_utils import (
    add_box
)


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


class AddBoxObject(bpy.types.Operator):
    bl_idname = 'mamoko.add_box_object'
    bl_label = "Add Box"
    bl_options = {'REGISTER', 'UNDO'}

    length: FloatProperty(
        name="Length",
        description="Length of the box object",
        default=1,
    )
    width: FloatProperty(
        name="Width",
        description="Width of the box object",
        default=1,
    )
    height: FloatProperty(
        name="Height",
        description="Height of the box object",
        default=1
    )

    # generic transform props
    align_items = (
        ('WORLD', "World", "Align the new object to the world"),
        ('VIEW', "View", "Align the new object to the view"),
        ('CURSOR', "3D Cursor",
         "Use the 3D cursor orientation for the new object")
    )
    align: EnumProperty(
        name="Align",
        items=align_items,
        default='WORLD',
        update=AddObjectHelper.align_update_callback,
    )
    location: FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
    )
    rotation: FloatVectorProperty(
        name="Rotation",
        subtype='EULER',
    )

    def execute(self, context) -> typing.Set:

        # verts, faces = add_box(self.width, self.height, self.length)

        mesh = bpy.data.meshes.new("Box")
        bm = bmesh.new()
        verts_dict = bmesh.ops.create_cube(
            bm,
            size=1,
            matrix=mathutils.Matrix.Identity(4),
            calc_uvs=True
        )
        bmesh.ops.scale(
            bm,
            vec=mathutils.Vector((self.length, self.width, self.height)),
            space=mathutils.Matrix.Identity(4),
            verts=bm.verts
        )

        bm.to_mesh(mesh)
        mesh.update()

        object_data_add(context, mesh, operator=self)

        return {'FINISHED'}
