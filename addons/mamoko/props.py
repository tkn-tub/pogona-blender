import bpy


_type_help = (
    "The type of the MaMoKo object.\n"
    "If this type is available as a class "
    "during the call to SceneManager.construct_from_config, "
    "a new instance will be constructed. "
)
_type_items_default = (
    ('INJECTOR', "Injector", _type_help + "A generic MaMoKo injector"),
    ('SENSOR', "Sensor", _type_help + "A generic MaMoKo sensor"),
    ('CUSTOM', "Custom", _type_help + "Specify the class name yourself"),
)


class MaMoKoTypeProperty(bpy.types.PropertyGroup):
    """
    A property for defining the type of a MaMoKo object.

    For objects included in the MaMoKo simulator, this should match its class
    name.
    If an object is not included, a 'Custom Type' can be defined.
    When calling `mamoko.SceneManager.construct_from_config()`,
    this custom type has to be present as a key in the
    `additional_component_classes` dictionary argument.
    """

    mamoko_type_enum: bpy.props.EnumProperty(
        name="Type",
        items=_type_items_default,
        default='CUSTOM',
        # update=mamoko_type_update_callback  # args: self, context
    )

    mamoko_type_custom: bpy.props.StringProperty(
        name="Custom Type",
        default=""
    )

    @property
    def mamoko_value(self):
        return (
            self.mamoko_type_enum
            if self.mamoko_type_enum != 'CUSTOM'
            else self.mamoko_type_custom
        )


_shape_items_default = (
    ('NONE', "NONE", "Use this for any MaMoKo Object that has a (custom) "
        "mesh, i.e., no sensors or injectors"),
    ('POINT', "POINT", "A single point. Useful, e.g., for a point injector"),
    ('SPHERE', "SPHERE", "A sphere of radius 0.5"),
    ('CYLINDER', "CYLINDER", "A cylinder of radius 0.5 and height 1"),
    ('CUBE', "CUBE", "A cube of side length 1"),
)


def _representation_update_shape_callback(self, context):
    bpy.ops.mamoko.update_representation_shape()


def _representation_update_scale_callback(self, context):
    bpy.ops.mamoko.update_representation_scale()


class MaMoKoRepresentationProperty(bpy.types.PropertyGroup):
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
    Whether or not an object is treated as a MaMoKo
    object is determined by whether it has an
    attribute `mamoko_flag` that is set to `True`
    (cp. class `MaMoKoPanel` in `panely.py`).
    """
    bpy.types.Object.mamoko_type = bpy.props.PointerProperty(
        name="Type",
        type=MaMoKoTypeProperty,
    )
    bpy.types.Object.mamoko_component_scale = bpy.props.FloatVectorProperty(
        name="Component Scale",
        description="The scale of the component as it will be applied in "
                    "the MaMoKo simulator. "
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
    bpy.types.Object.mamoko_shape = bpy.props.EnumProperty(
        name="Shape",
        items=_shape_items_default,
        default='NONE',
        update=_representation_update_shape_callback  # TODO: called twice?
    )
    bpy.types.Object.mamoko_representation = bpy.props.PointerProperty(
        name="Representation",
        type=MaMoKoRepresentationProperty,
    )
