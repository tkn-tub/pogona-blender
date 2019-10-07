import bpy
import bmesh
import mathutils
import bpy_extras


def _undo_unit_scale(context, bm):
    scale = 1 / context.scene.unit_settings.scale_length
    bmesh.ops.scale(
        bm,
        vec=mathutils.Vector((scale, scale, scale)),
        space=mathutils.Matrix.Identity(4),
        verts=bm.verts
    )


def _create_cube_mesh(context, mesh, bm):
    _ = bmesh.ops.create_cube(
        bm,
        size=1,
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    _undo_unit_scale(context, bm)
    bm.to_mesh(mesh)
    mesh.update()


def _create_cylinder_mesh(context, mesh, bm):
    _ = bmesh.ops.create_cone(
        bm,
        cap_ends=True,  # close ends
        segments=32,
        diameter1=0.5,  # actually radius, apparently
        diameter2=0.5,  # actually radius, apparently
        depth=1,
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    _undo_unit_scale(context, bm)
    bm.to_mesh(mesh)
    mesh.update()


def _create_sphere_mesh(context, mesh, bm):
    _ = bmesh.ops.create_uvsphere(
        bm,
        u_segments=32,
        v_segments=32,
        diameter=0.5,  # actually radius, apparently
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    _undo_unit_scale(context, bm)
    bm.to_mesh(mesh)
    mesh.update()


def _create_cross_mesh(context, mesh, bm):
    size = 0.5 / context.scene.unit_settings.scale_length
    verts = [
        mathutils.Vector((-size, 0, 0)),
        mathutils.Vector((size, 0, 0)),
        mathutils.Vector((0, -size, 0)),
        mathutils.Vector((0, size, 0)),
        mathutils.Vector((0, 0, -size)),
        mathutils.Vector((0, 0, size))
    ]
    edges = [
        (0, 1),
        (2, 3),
        (4, 5)
    ]
    mesh.from_pydata(verts, edges, [])


def _create_mamoko_object(self, context, create_mesh_func):
    mesh = bpy.data.meshes.new(f"MaMoKo {self.bl_label}")
    bm = bmesh.new()
    create_mesh_func(context, mesh, bm)
    bpy_extras.object_utils.object_data_add(context, mesh, operator=None)

    obj = context.active_object

    # Mark this object as part of the MaMoKo scene
    # (important for exporting and for toggling UI):
    obj['mamoko_flag'] = True

    # Apply scene unit scale to the object (not the mesh).
    # If you're working on a millimeter scale, for example,
    # this will scale down the 1 m objects to 1 mm in a way
    # that preserves your ability to set the scale in meters.
    scale = context.scene.unit_settings.scale_length
    obj.scale = [scale, scale, scale]

    return {'FINISHED'}


class MaMoKoRepresentationShapeUpdate(bpy.types.Operator):
    bl_idname = 'mamoko.update_representation_shape'
    bl_label = "Update Representation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if (obj.mamoko_representation.same_as_shape
                or obj.mamoko_representation.linked_object is None):
            mesh = bpy.data.meshes.new(obj.name)
            bm = bmesh.new()
            if obj.mamoko_shape == 'CUBE':
                _create_cube_mesh(context, mesh, bm)
            elif obj.mamoko_shape == 'CYLINDER':
                _create_cylinder_mesh(context, mesh, bm)
            elif obj.mamoko_shape == 'SPHERE':
                _create_sphere_mesh(context, mesh, bm)
            else:
                # obj.mamoko_shape in ('POINT', 'NONE'):
                _create_cross_mesh(context, mesh, bm)
            obj.data = mesh
        else:
            obj.data = obj.mamoko_representation.linked_object.data

        return {'FINISHED'}


class MaMoKoRepresentationScaleUpdate(bpy.types.Operator):
    """
    Update the scale in Blender based on the MaMoKo component scale and
    the additional visualization scale.
    """
    bl_idname = 'mamoko.update_representation_scale'
    bl_label = "Update scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        unit_scale = context.scene.unit_settings.scale_length
        new_scale = [
            obj.mamoko_component_scale[i]
            * unit_scale  # component_scale is defined as LENGTH
            * obj.mamoko_representation.additional_scale[i]  # this is not
            for i in range(3)
        ]
        obj.scale = new_scale
        return {'FINISHED'}


class MaMoKoAddCube(bpy.types.Operator):
    bl_idname = 'mamoko.add_cube'
    bl_label = "Cube"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_mamoko_object(self, context, _create_cube_mesh)
        obj = context.active_object
        obj.mamoko_shape = 'CUBE'
        return {'FINISHED'}


class MaMoKoAddCylinder(bpy.types.Operator):
    bl_idname = 'mamoko.add_cylinder'
    bl_label = "Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_mamoko_object(self, context, _create_cylinder_mesh)
        obj = context.active_object
        obj.mamoko_shape = 'CYLINDER'
        return {'FINISHED'}


class MaMoKoAddSphere(bpy.types.Operator):
    bl_idname = 'mamoko.add_sphere'
    bl_label = "Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_mamoko_object(self, context, _create_sphere_mesh)
        obj = context.active_object
        obj.mamoko_shape = 'SPHERE'
        return {'FINISHED'}


class MaMoKoAddPoint(bpy.types.Operator):
    bl_idname = 'mamoko.add_point'
    bl_label = "Point"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _create_mamoko_object(self, context, _create_cross_mesh)
        obj = context.active_object
        obj.mamoko_shape = 'POINT'
        return {'FINISHED'}
