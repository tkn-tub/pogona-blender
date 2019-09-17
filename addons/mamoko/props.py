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


def _representation_update_callback(self, context):
    bpy.ops.mamoko.update_representation()


class MaMoKoRepresentationProperty(bpy.types.PropertyGroup):
    same_as_shape: bpy.props.BoolProperty(
        name="Same As Shape",
        default=True,
        update=_representation_update_callback,
    )
    linked_object: bpy.props.PointerProperty(
        name="Target",
        type=bpy.types.Object,
        update=_representation_update_callback
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
    bpy.types.Object.mamoko_shape = bpy.props.EnumProperty(
        name="Shape",
        items=_shape_items_default,
        default='NONE',
        update=_representation_update_callback
    )
    bpy.types.Object.mamoko_representation = bpy.props.PointerProperty(
        name="Representation",
        type=MaMoKoRepresentationProperty,
    )
