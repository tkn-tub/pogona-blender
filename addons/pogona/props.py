import bpy
import os
from . import util


_type_help = (
    "The type of the Pogona object.\n"
    "If this type is available as a class "
    "during the call to SceneManager.construct_from_config, "
    "a new instance will be constructed. "
)
_type_items_default = (
    ('INJECTOR', "Injector", _type_help + "A generic Pogona injector"),
    ('SENSOR', "Sensor", _type_help + "A generic Pogona sensor"),
    ('CUSTOM', "Custom", _type_help + "Specify the class name yourself"),
)


class PogonaTypeProperty(bpy.types.PropertyGroup):
    """
    A property for defining the type of a Pogona object.

    For objects included in the Pogona simulator, this should match its class
    name.
    If an object is not included, a 'Custom Type' can be defined.
    When calling `pogona.SceneManager.construct_from_config()`,
    this custom type has to be present as a key in the
    `additional_component_classes` dictionary argument.
    """

    pogona_type_enum: bpy.props.EnumProperty(
        name="Type",
        items=_type_items_default,
        default='CUSTOM',
        # update=pogona_type_update_callback  # args: self, context
    )

    pogona_type_custom: bpy.props.StringProperty(
        name="Custom Type",
        default=""
    )

    @property
    def pogona_value(self):
        return (
            self.pogona_type_enum
            if self.pogona_type_enum != 'CUSTOM'
            else self.pogona_type_custom
        )


_shape_items_default = (
    ('NONE', "NONE", "Use this for any Pogona Object that has a (custom) "
        "mesh, i.e., no sensors or injectors"),
    ('POINT', "POINT", "A single point. Useful, e.g., for a point injector"),
    ('SPHERE', "SPHERE", "A sphere of radius 0.5"),
    ('CYLINDER', "CYLINDER", "A cylinder of radius 0.5 and height 1"),
    ('CUBE', "CUBE", "A cube of side length 1"),
)


def _representation_update_shape_callback(self, context):
    bpy.ops.pogona.update_representation_shape()


def _representation_update_scale_callback(self, context):
    bpy.ops.pogona.update_representation_scale()


def _molecule_positions_path_update_callback(self, context):
    # Adjust minimum and maximum step
    obj = context.active_object
    path = bpy.path.abspath(obj.pogona_molecule_positions_path)
    # bpy.path.abspath may still produce paths like
    # `/home/user/path/to/blendfile/../../../selected-folder/`
    # Can be resolved with os.path.abspath:
    path = os.path.abspath(path)
    steps = []
    try:
        for filename in os.listdir(path):
            m = util.MOLECULE_POSITIONS_CSV_PATTERN.match(filename)
            if not m:
                continue
            steps.append(int(m.group('step')))
        if '_RNA_UI' not in obj:
            obj['_RNA_UI'] = dict()
        if 'pogona_molecule_positions_step' not in obj['_RNA_UI']:
            obj['_RNA_UI']['pogona_molecule_positions_step'] = dict()
        min_steps = min(steps)
        max_steps = max(steps)
        obj['_RNA_UI']['pogona_molecule_positions_step'].update(dict(
            min=min_steps,
            max=max_steps,
            soft_min=min_steps,
            soft_max=max_steps,
        ))
        print(f"Set minimum step for object '{obj.name}' to "
              f"{min_steps} and the maximum to {max_steps}.")
    except FileNotFoundError as e:
        raise Warning("Could not find the molecule positions path of "
                      f"object '{obj.name}'.")

    # Trigger a frame change without changing the frame
    # to update the mesh:
    context.scene.frame_current = context.scene.frame_current


def _molecule_positions_time_update_callback(self, context):
    # Trigger a frame change without changing the frame
    # to update the mesh:
    context.scene.frame_current = context.scene.frame_current


class PogonaRepresentationProperty(bpy.types.PropertyGroup):
    """
    What shape a component is supposed to take on in Blender.
    If it is different from the component's shape (e.g., unlike a sensor
    component, a y-connector tube cannot be represented by the default
    shapes), a custom shape can be defined by linking to another (possibly
    hidden) Blender object.
    """
    same_as_shape: bpy.props.BoolProperty(
        name="Same As Shape",
        default=True,
        update=_representation_update_shape_callback,
    )
    linked_object: bpy.props.PointerProperty(
        name="Target",
        type=bpy.types.Object,
        update=_representation_update_shape_callback
    )
    additional_scale: bpy.props.FloatVectorProperty(
        name="Additional scale",
        description="This scale will be applied on top of the scale defined "
                    "for the component itself. "
                    "This can be useful for making components more visible "
                    "that are otherwise overlapping with others, "
                    "or if you are using a built-in shape for representing "
                    "an OpenFOAM mesh which itself is already scaled.",
        default=(1, 1, 1),
        subtype='XYZ',
        precision=6,  # maximum number of decimal digits to display
        # (unit='LENGTH',)  no unit for additional scale
        update=_representation_update_scale_callback,
    )


def add_custom_properties_to_object_class():
    """
    Make all Blender objects have these properties.
    Whether or not an object is treated as a Pogona
    object is determined by whether it has an
    attribute `pogona_flag` that is set to `True`
    (cp. class `PogonaPanel` in `panely.py`).
    """
    bpy.types.Object.pogona_type = bpy.props.PointerProperty(
        name="Type",
        type=PogonaTypeProperty,
    )
    bpy.types.Object.pogona_component_scale = bpy.props.FloatVectorProperty(
        name="Component Scale",
        description="The scale of the component as it will be applied in "
                    "the Pogona simulator. "
                    "For the built-in shapes, this will correspond to the "
                    "width, height, and depth of the component in meters.",
        default=(1, 1, 1),  # TODO: ensure this is updated when bl obj is
                            #  scaled in viewport! (seems like that's not
                            #  really possible)
        subtype='XYZ',
        precision=6,  # maximum number of decimal digits to display
        unit='LENGTH',
        update=_representation_update_scale_callback,
    )
    bpy.types.Object.pogona_shape = bpy.props.EnumProperty(
        name="Shape",
        items=_shape_items_default,
        default='NONE',
        update=_representation_update_shape_callback  # TODO: called twice?
    )
    bpy.types.Object.pogona_representation = bpy.props.PointerProperty(
        name="Representation",
        type=PogonaRepresentationProperty,
    )

    # Molecules visualization properties:
    bpy.types.Object.pogona_molecule_positions_path = bpy.props.StringProperty(
        name="Molecule Positions Path",
        description="A folder with Pogona simulation results in the form of "
                    "CSV files named `positions.csv.<time step>`. "
                    "These files should have the following columns: "
                    "(molecule) `id`, `x`, `y`, `z`, `cell_id`, `object_id`.",
        subtype='DIR_PATH',
        update=_molecule_positions_path_update_callback
    )
    bpy.types.Object.pogona_molecule_positions_step = bpy.props.IntProperty(
        name="Time Step",
        description="Time step N corresponding to the suffix of a "
                    "`positions.csv.<N>` file.",
        options={'ANIMATABLE'},
        update=_molecule_positions_time_update_callback,
    )
