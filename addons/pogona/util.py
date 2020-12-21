# Pogona Blender add-on
# Copyright (C) 2020 Data Communications and Networking (TKN), TU Berlin
#
# This file is part of Pogona, a simulator for macroscopic molecular
# communication.
#
# Pogona is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pogona is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pogona.  If not, see <https://www.gnu.org/licenses/>.import bpy

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
