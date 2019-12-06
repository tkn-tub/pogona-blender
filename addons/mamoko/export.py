import bpy
from bpy_extras.io_utils import ExportHelper
import yaml
from typing import Dict


def _check_object_scale(
        operator: bpy.types.Operator,
        obj: bpy.types.Object,
        context: bpy.types.Context,
) -> bool:
    epsilon = .00001
    ok = True
    unit_scale = context.scene.unit_settings.scale_length
    expected = [
        obj.mamoko_component_scale[i]
        * unit_scale  # component_scale is defined as LENGTH
        * obj.mamoko_representation.additional_scale[i]  # this is not
        for i in range(3)
    ]
    for i in range(3):
        s = obj.scale[i]
        if not expected[i] - epsilon < s < expected[i] + epsilon:
            operator.report(
                {'WARNING'},
                f"The scale of component \"{obj.name}\" in Blender "
                f"({list(obj.scale)}) deviates from the MaMoKo scale "
                "defined via the component scale and the additional "
                "visualization scale, which should combine to "
                f"{list(expected)}. "
                "This can happen when you change a component's scale "
                "in the viewport rather than via its MaMoKo "
                "properties."
            )
            ok = False
            break
    return ok


class MaMoKoExporter(bpy.types.Operator, ExportHelper):
    """Export scene for the MaMoKo simulator."""

    bl_idname = 'mamoko.exporter'
    bl_label = "MaMoKo Scene (.scene.yaml)"

    # Used by ExportHelper:
    filename_ext = '.yaml'

    filter_glob: bpy.props.StringProperty(
        default='*.yaml',
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        components: Dict[str, Dict] = dict()
        for obj in bpy.context.scene.objects:
            if 'mamoko_type' not in obj or 'mamoko_shape' not in obj:
                continue
            print(f"Exporting object of type {obj['mamoko_type']}")

            unit_scale = context.scene.unit_settings.scale_length

            components[obj.name] = dict(
                # type=obj.mamoko_type.mamoko_value,
                # ^ object type should now be written to the config.yaml,
                # not scene.yaml
                shape=obj.mamoko_shape,
                rotation=list(obj.rotation_euler),
                translation=list(obj.location * unit_scale),
                # ^ TODO: checkbox: apply unit scale
                # Component scale is defined as LENGTH, apply unit scale:
                scale=list(obj.mamoko_component_scale * unit_scale),
                # Additional visualization scale not defined as LENGTH,
                # therefore no unit scale:
                visualization_scale=list(
                    obj.mamoko_representation.additional_scale
                ),
            )

            _check_object_scale(operator=self, obj=obj, context=context)

        data = dict(
            components=components,
        )

        with open(self.filepath, 'w') as f:
            yaml.dump(data, stream=f, default_flow_style=False)

        return {'FINISHED'}


def menu_func_export(self, context):
    self.layout.operator(
        MaMoKoExporter.bl_idname,
        text=MaMoKoExporter.bl_label
    )
