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
        row = layout.row()
        row.template_list(
            'POGONA_UL_ParticleAttrUIList',
            list_id='Pogona Particle Attributes List',
            dataptr=obj,
            propname='pogona_molecule_attributes',
            active_dataptr=obj,  # where to find the index
            active_propname='pogona_molecule_attributes_selected_index',
        )
        row = layout.row()
        row.operator(
            'pogona_particle_attr_list.new_item',
            text="New",
        )
        row.operator(
            'pogona_particle_attr_list.delete_item',
            text="Remove",
        )
        if (
                obj.pogona_molecule_attributes_selected_index >= 0
                and len(obj.pogona_molecule_attributes) > 0
                # and obj.pogona_molecule_attributes_selected_index
        ):
            row = layout.row()
            item = obj.pogona_molecule_attributes[
                obj.pogona_molecule_attributes_selected_index
            ]
            row.prop(item, 'pogona_particle_attr')
            row = layout.row()
            row.prop(item, 'pogona_particle_attr_type')


class POGONA_UL_ParticleAttrUIList(bpy.types.UIList):
    """
    User interface for Pogona particle attribute lists for
    particle visualizations and use with Geometry Nodes.

    UI based on this tutorial:
    https://sinestesia.co/blog/tutorials/using-uilists-in-blender/
    """

    def draw_item(
            self,
            context,
            layout,
            data,
            item,
            icon,
            active_data,
            active_propname,
            index
    ):
        # Make sure to support all 3 layout types:
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(
                text=f"{item.pogona_particle_attr}: "
                     f"{item.pogona_particle_attr_type}",
                icon='OBJECT_DATAMODE',
            )
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER',
            layout.label(text="", icon='OBJECT_DATAMODE')


class LIST_OT_NewPogonaParticleAttr(bpy.types.Operator):
    """Add a new item to the UI list"""

    bl_idname = 'pogona_particle_attr_list.new_item'
    bl_label = "Add a new attribute"

    def execute(self, context):
        vis_obj = context.object
        vis_obj.pogona_molecule_attributes.add()
        return {'FINISHED'}

class LIST_OT_DeletePogonaParticleAttr(bpy.types.Operator):
    """Delete a selected item from the UI list"""

    bl_idname = 'pogona_particle_attr_list.delete_item'
    bl_label = "Delete attribute"

    @classmethod
    def poll(self, context):
        return context.object.pogona_molecule_attributes

    def execute(self, context):
        ui_list = context.object.pogona_molecule_attributes
        list_index = context.object.pogona_molecule_attributes_selected_index
        ui_list.remove(list_index)
        context.object.pogona_molecule_attributes_selected_index = min(
            max(0, list_index - 1),
            len(ui_list) - 1
        )
        return {'FINISHED'}
