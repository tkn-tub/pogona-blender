import bpy


class PogonaPanel(bpy.types.Panel):
    """
    Creates a panel in the object context of the properties editor.
    """
    bl_label = "Pogona"
    bl_idname = 'OBJECT_PT_pogonapanel'
    bl_space_type = 'PROPERTIES'  # or VIEW_3D?
    bl_region_type = 'WINDOW'
    bl_order = 0  # in [0, inf], lower -> higher
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        """If this returns True, the panel will be drawn."""
        return (
            context.object is not None
            and context.object.get('pogona_flag', False)
        )

    def draw(self, context):
        layout = self.layout
        obj = context.object

        layout.label(text="Basic Properties")
        row = layout.row()
        row.prop(obj, 'name')
        layout.separator()

        # Object type:
        pogona_type = obj.pogona_type
        row = layout.row()
        row.prop(pogona_type, 'pogona_type_enum')
        row = layout.row()
        row.prop(pogona_type, 'pogona_type_custom')
        row.enabled = pogona_type.pogona_type_enum == 'CUSTOM'
        layout.separator()

        # Shape and scale:
        row = layout.row()
        row.prop(obj, 'pogona_shape')
        box = layout.box()
        box.prop(obj, 'pogona_component_scale')
        layout.separator()

        # Representation (in Blender):
        layout.label(text="Representation (in Blender)")
        pogona_representation = obj.pogona_representation
        row = layout.row()
        row.prop(pogona_representation, 'same_as_shape')
        row = layout.row()
        row.prop(pogona_representation, 'linked_object')
        row.enabled = not pogona_representation.same_as_shape
        box = layout.box()
        box.prop(pogona_representation, 'additional_scale')


class PogonaMoleculesVisualizationPanel(bpy.types.Panel):
    """
    Creates a panel in the object context of the properties editor,
    but only for objects with the 'pogona_molecule_visualization_flag'
    set to True.
    """
    bl_label = "Pogona Molecules Visualization"
    bl_idname = 'OBJECT_PT_pogonamoleculevispanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_order = 0  # in [0, inf], lower -> higher
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        """If this returns True, the panel will be drawn."""
        return (
            context.object is not None
            and context.object.get('pogona_molecule_visualization_flag', False)
        )

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.prop(obj, 'pogona_molecule_positions_path')
        row = layout.row()
        row.prop(obj, 'pogona_molecule_positions_step')