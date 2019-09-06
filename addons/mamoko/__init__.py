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

if 'bpy' in locals():
    import importlib
    importlib.reload(props)
    importlib.reload(ops)
    importlib.reload(export)
    importlib.reload(panel)
else:
    from . import props
    from . import ops
    from . import export
    from . import panel

import bpy
from bpy.types import AddonPreferences
from bpy.props import (
    StringProperty,
)
from bpy.types import Menu


class MaMoKoPreferences(AddonPreferences):
    bl_idname = 'mamoko.preferences'

    objects_path: StringProperty(
        name="Objects path",
        description=(
            "Path to your MaMoKo objects"
        ),
        default="",
        subtype='DIR_PATH',
        # TODO: update function, 
        #   see https://docs.blender.org/api/current/bpy.props.html
        # update=my_update_func
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="MaMoKo Preferences")
        layout.prop(self, "objects_path")


class VIEW3D_MT_mesh_mamoko_add(Menu):
    """Define the "Add MaMoKo object" menu."""
    bl_idname = 'VIEW3D_MT_mesh_mamoko_add'
    bl_label = "MaMoKo"

    def draw(self, context):
        layout = self.layout
        layout.menu(
            VIEW3D_MT_mesh_mamoko_add_shapes.bl_idname,
            icon='NONE'
        )
        # layout.separator()


class VIEW3D_MT_mesh_mamoko_add_shapes(Menu):
    """Shape Presets submenu"""
    bl_idname = 'VIEW3D_MT_mesh_mamoko_add_shapes'
    bl_label = "Shape Presets"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator(ops.MaMoKoAddCube.bl_idname, icon='MESH_CUBE')
        layout.operator(
            ops.MaMoKoAddCylinder.bl_idname,
            icon='MESH_CYLINDER'
        )
        layout.operator(
            ops.MaMoKoAddSphere.bl_idname,
            icon='MESH_UVSPHERE'
        )
        layout.operator(ops.MaMoKoAddPoint.bl_idname, icon='EMPTY_AXIS')


def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.menu(
        VIEW3D_MT_mesh_mamoko_add.bl_idname,
        text=VIEW3D_MT_mesh_mamoko_add.bl_label,
        icon='PLUGIN'
    )


classes = (
    props.MaMoKoTypeProperty,
    props.MaMoKoRepresentationProperty,
    ops.MaMoKoRepresentationUpdate,
    ops.MaMoKoAddCube,
    ops.MaMoKoAddPoint,
    ops.MaMoKoAddSphere,
    ops.MaMoKoAddCylinder,
    MaMoKoPreferences,
    VIEW3D_MT_mesh_mamoko_add,
    VIEW3D_MT_mesh_mamoko_add_shapes,
    export.MaMoKoExporter,
    panel.MaMoKoPanel,
)


def register():
    print("Registering MaMoKo…")

    for cls in classes:
        print(f"Registering class \"{cls}\"")
        bpy.utils.register_class(cls)

    props.add_custom_properties_to_object_class()

    # Populate menu:
    bpy.types.VIEW3D_MT_add.append(menu_func)
    bpy.types.TOPBAR_MT_file_export.append(export.menu_func_export)

    print("MaMoKo: ready")


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.types.TOPBAR_MT_file_export.remove(export.menu_func_export)

    print("Unregistered MaMoKo")
