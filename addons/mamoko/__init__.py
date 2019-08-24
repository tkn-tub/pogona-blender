import bpy
from bpy.types import AddonPreferences
from bpy.props import (
    StringProperty,
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
    bl_idname = __name__

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


def register():
    print("Registered MaMoKo")

    bpy.utils.register_class(MaMoKoPreferences)


def unregister():
    bpy.utils.unregister_class(MaMoKoPreferences)

    print("Unregistered MaMoKo")
