import bpy
from bpy_extras.io_utils import ExportHelper
import yaml
from typing import Dict


class MaMoKoExporter(bpy.types.Operator, ExportHelper):
    """Export scene for the MaMoKo simulator."""

    bl_idname = 'mamoko.exporter'
    bl_label = "MaMoKo Scene"

    # Used by ExportHelper:
    filename_ext = '.yaml'  # TODO: .yaml files don't show up in file explorer

    filter_glob: bpy.props.StringProperty(
        default='.yaml',
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        data: Dict[str, Dict] = dict()
        for obj in bpy.context.scene.objects:
            if 'mamoko_type' not in obj or 'mamoko_shape' not in obj:
                continue
            print(f"Exporting object of type {obj['mamoko_type']}")

            data[obj.name] = dict(
                type=obj.mamoko_type.mamoko_value,
                shape=obj['mamoko_shape'],
                rotation=list(obj.rotation_euler),
                translation=list(obj.location),
                scale=list(obj.scale),
            )

        with open(self.filepath, 'w') as f:
            yaml.dump(data, stream=f, default_flow_style=False)

        return {'FINISHED'}


def menu_func_export(self, context):
    self.layout.operator(
        MaMoKoExporter.bl_idname,
        text=MaMoKoExporter.bl_label
    )
