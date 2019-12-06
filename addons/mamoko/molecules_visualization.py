import bpy
from bpy.app.handlers import persistent


@persistent
def _update_all_molecule_visualizations(scene):
    print(f"Updating molecule visualizations, frame {scene.frame_current}")
    for obj in scene.objects:
        if 'mamoko_molecule_visualization_flag' not in obj or \
                not obj['mamoko_molecule_visualization_flag']:
            continue

        # TODO: check properties of this object for the folder of the CSVs
        #  then check properties to figure out timing information
        #  then load the correct CSV
        #  then replace the object's mesh
        #  (and free the old mesh from memory if possible)


def register_handlers():
    bpy.app.handlers.frame_change_pre.append(
        _update_all_molecule_visualizations
    )


def unregister_handlers():
    bpy.app.handlers.frame_change_pre.remove(
        _update_all_molecule_visualizations
    )
