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

bl_info = {
    "name": "Pogona Scenes Tool",
    "author": "Lukas Stratmann (lukas@lukas-stratmann.com)",
    "description": (
        "Tools for creating and inspecting scenes for the "
        "Pogona molecular communication simulator."
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
    importlib.reload(molecules_visualization)
else:
    from . import props
    from . import ops
    from . import export
    from . import panel
    from . import molecules_visualization

import bpy
from bpy.types import AddonPreferences
from bpy.props import (
    StringProperty,
)
from bpy.types import Menu


class PogonaPreferences(AddonPreferences):
    bl_idname = 'pogona.preferences'

    objects_path: StringProperty(
        name="Objects path",
        description=(
            "Path to your Pogona OpenFOAM objects"
        ),
        default="",
        subtype='DIR_PATH',
        # TODO: update function, 
        #   see https://docs.blender.org/api/current/bpy.props.html
        # update=my_update_func
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Pogona Preferences")
        layout.prop(self, "objects_path")


class VIEW3D_MT_mesh_pogona_add(Menu):
    """Define the "Add Pogona object" menu."""
    bl_idname = 'VIEW3D_MT_mesh_pogona_add'
    bl_label = "Pogona"

    def draw(self, context):
        layout = self.layout
        layout.menu(
            VIEW3D_MT_mesh_pogona_add_shapes.bl_idname,
            icon='NONE'
        )
        layout.operator(
            ops.PogonaAddMoleculesVisualization.bl_idname,
            icon='PARTICLES'
        )
        # layout.separator()


class VIEW3D_MT_mesh_pogona_add_shapes(Menu):
    """Shape Presets submenu"""
    bl_idname = 'VIEW3D_MT_mesh_pogona_add_shapes'
    bl_label = "Shape Presets"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator(ops.PogonaAddCube.bl_idname, icon='MESH_CUBE')
        layout.operator(
            ops.PogonaAddCylinder.bl_idname,
            icon='MESH_CYLINDER'
        )
        layout.operator(
            ops.PogonaAddSphere.bl_idname,
            icon='MESH_UVSPHERE'
        )
        layout.operator(ops.PogonaAddPoint.bl_idname, icon='EMPTY_AXIS')


def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.menu(
        VIEW3D_MT_mesh_pogona_add.bl_idname,
        text=VIEW3D_MT_mesh_pogona_add.bl_label,
        icon='PLUGIN'
    )


classes = (
    props.PogonaTypeProperty,
    props.PogonaRepresentationProperty,
    ops.PogonaRepresentationShapeUpdate,
    ops.PogonaRepresentationScaleUpdate,
    ops.PogonaAddCube,
    ops.PogonaAddPoint,
    ops.PogonaAddSphere,
    ops.PogonaAddCylinder,
    ops.PogonaAddMoleculesVisualization,
    PogonaPreferences,
    VIEW3D_MT_mesh_pogona_add,
    VIEW3D_MT_mesh_pogona_add_shapes,
    export.PogonaExporter,
    panel.PogonaPanel,
    panel.PogonaMoleculesVisualizationPanel,
)


def register():
    print("Registering Pogona…")

    for cls in classes:
        print(f"Registering class \"{cls}\"")
        bpy.utils.register_class(cls)

    props.add_custom_properties_to_object_class()

    # Populate menu:
    bpy.types.VIEW3D_MT_add.append(menu_func)
    bpy.types.TOPBAR_MT_file_export.append(export.menu_func_export)

    molecules_visualization.register_handlers()

    print("Pogona: ready")


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.types.TOPBAR_MT_file_export.remove(export.menu_func_export)

    molecules_visualization.unregister_handlers()

    print("Unregistered Pogona")
