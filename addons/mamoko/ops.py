import bpy
import bmesh
import mathutils
import bpy_extras
import functools


def _create_cube_mesh(mesh, bm):
    _ = bmesh.ops.create_cube(
        bm,
        size=1,
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    bm.to_mesh(mesh)
    mesh.update()


def _create_cylinder_mesh(mesh, bm):
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
    bm.to_mesh(mesh)
    mesh.update()


def _create_sphere_mesh(mesh, bm):
    _ = bmesh.ops.create_uvsphere(
        bm,
        u_segments=32,
        v_segments=32,
        diameter=0.5,  # actually radius, apparently
        matrix=mathutils.Matrix.Identity(4),
        calc_uvs=True
    )
    bm.to_mesh(mesh)
    mesh.update()


def _create_cross_mesh(mesh, bm):
    size = 0.5
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
    create_mesh_func(mesh, bm)
    bpy_extras.object_utils.object_data_add(context, mesh, operator=None)

    # Mark this object as part of the MaMoKo scene
    # (important for exporting and for toggling UI):
    context.active_object['mamoko_flag'] = True

    return {'FINISHED'}


class MaMoKoRepresentationUpdate(bpy.types.Operator):
    bl_idname = f'mamoko.update_representation'
    bl_label = "Update Representation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if (obj.mamoko_representation.same_as_shape 
                or obj.mamoko_representation.linked_object is None):
            mesh = bpy.data.meshes.new(obj.name)
            bm = bmesh.new()
            if obj.mamoko_shape == 'CUBE':
                _create_cube_mesh(mesh, bm)
            elif obj.mamoko_shape == 'CYLINDER':
                _create_cylinder_mesh(mesh, bm)
            elif obj.mamoko_shape == 'SPHERE':
                _create_sphere_mesh(mesh, bm)
            else:
                # obj.mamoko_shape in ('POINT', 'NONE'):
                _create_cross_mesh(mesh, bm)
            obj.data = mesh
        else:
            obj.data = obj.mamoko_representation.linked_object.data

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
        return _create_mamoko_object(self, context, _create_cross_mesh)
        obj = context.active_object
        obj.mamoko_shape = 'POINT'
        return {'FINISHED'}
