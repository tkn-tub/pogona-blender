import bpy


class MaMoKoPanel(bpy.types.Panel):
    """
    Creates a panel in the object context of the properties editor.
    """
    bl_label = "MaMoKo"
    bl_idname = 'OBJECT_PT_mamokopanel'
    bl_space_type = 'PROPERTIES'  # or VIEW_3D?
    bl_region_type = 'WINDOW'
    bl_order = 0  # in [0, inf], lower -> higher
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        """If this returns True, the panel will be drawn."""
        return (
            context.object is not None
            and context.object.get('mamoko_flag', False)
        )

    def draw(self, context):
        layout = self.layout
        obj = context.object

        layout.label(text="Basic Properties")
        row = layout.row()
        row.prop(obj, 'name')
        layout.separator()

        # Object type:
        mamoko_type = obj.mamoko_type
        row = layout.row()
        row.prop(mamoko_type, 'mamoko_type_enum')
        row = layout.row()
        row.prop(mamoko_type, 'mamoko_type_custom')
        row.enabled = mamoko_type.mamoko_type_enum == 'CUSTOM'
        layout.separator()

        # Shape and scale:
        row = layout.row()
        row.prop(obj, 'mamoko_shape')
        box = layout.box()
        box.prop(obj, 'mamoko_component_scale')
        layout.separator()

        # Representation (in Blender):
        layout.label(text="Representation (in Blender)")
        mamoko_representation = obj.mamoko_representation
        row = layout.row()
        row.prop(mamoko_representation, 'same_as_shape')
        row = layout.row()
        row.prop(mamoko_representation, 'linked_object')
        row.enabled = not mamoko_representation.same_as_shape
        box = layout.box()
        box.prop(mamoko_representation, 'additional_scale')


class MaMoKoMoleculesVisualizationPanel(bpy.types.Panel):
    """
    Creates a panel in the object context of the properties editor,
    but only for objects with the 'mamoko_molecule_visualization_flag'
    set to True.
    """
    bl_label = "MaMoKo Molecules Visualization"
    bl_idname = 'OBJECT_PT_mamokomoleculevispanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_order = 0  # in [0, inf], lower -> higher
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        """If this returns True, the panel will be drawn."""
        return (
            context.object is not None
            and context.object.get('mamoko_molecule_visualization_flag', False)
        )

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.prop(obj, 'mamoko_molecule_positions_path')
        row = layout.row()
        row.prop(obj, 'mamoko_molecule_positions_step')
