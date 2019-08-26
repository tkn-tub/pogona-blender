import bpy
from bpy.types import AddonPreferences
from bpy.props import (
    StringProperty,
)
from .add_object import (
    get_operator_for_object,
    AddBoxObject,
)

bl_info = {
    "name": "MaMoKo Scenes Tool",
    "author": "Lukas Stratmann (lukas@lukas-stratmann.com)",
    "description": (
        "Tools for creating and inspecting scenes for the "
        "MaMoKo molecular communication simulator."
    ),
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D View",
    "warning": "",
    "wiki_url": "",
    "support": 'COMMUNITY',
    "category": "3D View"
}


class MaMoKoPreferences(AddonPreferences):
    bl_idname = 'mamoko.preferences'

    objects_path: StringProperty(
        name="Objects path",
        description=(
            "Path to your MaMoKo objects"
        ),
        default="",
        subtype='DIR_PATH',
        # TODO: update function, see https://docs.blender.org/api/current/bpy.props.html
        # update=my_update_func
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="MaMoKo Preferences")
        layout.prop(self, "objects_path")


classes = (
    MaMoKoPreferences,
    AddBoxObject,
)


def add_cube_object(self, context):
    self.layout.operator(AddBoxObject.bl_idname, icon='PLUGIN')


def register():
    print("Registered MaMoKo")

    for cls in classes:
        bpy.utils.register_class(cls)

    # Populate menu:
    bpy.types.VIEW3D_MT_add.append(add_cube_object)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("Unregistered MaMoKo")
