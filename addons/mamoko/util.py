import bpy
import re


MOLECULE_POSITIONS_CSV_PATTERN = re.compile(r'positions.csv.(?P<step>\d+)')


def delete_mesh(mesh: bpy.types.Mesh, clear_users=True):
    if mesh.users > 0:
        print(
            f"Not deleting mesh '{mesh.name}' because it still has "
            f"{mesh.users} users."
        )
        return False
    try:
        if clear_users:
            mesh.user_clear()
        bpy.data.meshes.remove(mesh)
        return True
    except Exception as e:
        raise Warning(f"Mesh '{mesh.name}' not deleted because of this "
                      f"exception: {e}")
        return False
