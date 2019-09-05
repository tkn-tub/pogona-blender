import bpy
import bmesh
import mathutils


class MaMoKoRepresentationUpdate(bpy.types.Operator):
    bl_idname = f'mamoko.update_representation'
    bl_label = "Update Representation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if obj.mamoko_representation.same_as_shape:
            mesh = bpy.data.meshes.new(obj.name)
            bm = bmesh.new()
            if obj.mamoko_shape == 'CUBE':
                _ = bmesh.ops.create_cube(
                    bm,
                    size=1,
                    matrix=mathutils.Matrix.Identity(4),
                    calc_uvs=True
                )
                bm.to_mesh(mesh)
            elif obj.mamoko_shape == 'CYLINDER':
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
            elif obj.mamoko_shape == 'SPHERE':
                _ = bmesh.ops.create_uvsphere(
                    bm,
                    u_segments=32,
                    v_segments=32,
                    diameter=0.5,  # actually radius, apparently
                    matrix=mathutils.Matrix.Identity(4),
                    calc_uvs=True
                )
                bm.to_mesh(mesh)
            else:
                # obj.mamoko_shape in ('POINT', 'NONE'):
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
            obj.data = mesh
        else:
            # Try to use linked object
            obj.data = obj.mamoko_representation.linked_object.data
            # TODO: check if linked object is set; if not, use point again!

        # TODO: delete old mesh!
        return {'FINISHED'}  # TODO?

