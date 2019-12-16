# MaMoKo Blender Add-on

The Blender Add-on for creating and inspecting scenes for our MaMoKo simulator

## Installation

After following the installation instructions below (respective for your use case), make sure to select the 'Objects path' in the add-on preferences!
This path should point to the directory where all MaMoKo simulator objects are defined.
(TODO: We need a common way of defining objects; right now such a folder does not really exist yet.)

### For Users

1. Create a zip file from the `addons/mamoko/` folder.
    An easy way to do this is simply to run `make` in this directory.
2. This add-on depends on some Python packages Blender doesn't ship with by default (e.g., for saving YAML configuration files). Install these dependencies:
    1. Find the Python binary that came bundled with your installation of Blender. If you downloaded Blender as a compressed archive, it will be in `<path to where you extracted the files>/<Blender version, e.g. '2.81'>/python/bin/python<python version>`. Let's call it simply `python` from here on. If you installed Blender using a package manager (e.g., pacman), it may suffice to install the required packages with your regular python/pip.
    2. Run `python -m ensurepip`
    3. `python -m pip install -r requirements.txt`
3. Open Blender.
4. Navigate to "Edit" > "Preferences…" > "Add-ons", then click "Install…" and select the zip file from step 1.

### For Add-on Developers

Install Python requirements (see step 2. in the section above).

There are several options for installing the add-on:

1. Define an alternative scripts path in the Blender preferences.
    1. Go to "Edit" > "Preferences…" > "File Paths" and enter the path to this directory.
2. Link the `addons/mamoko/` directory of this cloned repository into a valid Blender add-ons path, e.g., `~/.config/blender/2.80/scripts/addons/` (see https://docs.blender.org/manual/en/latest/advanced/scripting/introduction.html#file-location for other operating systems).

Having used either of these options, the MaMoKo add-on should now appear in the list of available Add-ons in the Blender preferences.
After making a change, simply disable and re-enable the add-on. (This actually only seems to work in the rarest of cases. When in doubt, restart Blender.)

## Basic Workflow

- Open an empty scene in Blender (yes, you will likely delete the default cube just to add another cube soon after – but it'll be a special cube!)
- In the scene properties, set the unit scale to something sensible (e.g., 0.001 if you are working at the scale of millimeters).
- Add one or more MaMoKo objects: Hit Shift+A (or click on "Add" in the 3D viewport) and select the desired object template from the "MaMoKo" submenu.
- Select an object and adjust its properties in the properties window under the "Object" context in the "MaMoKo" panel. Don't forget to give it a recognizeable name!
- Transform the object as desired. The location, rotation, and scale of the object will be written out to the scene.yaml later on. If the "Same as Shape" checkbox for the representation is checked, do not use edit mode for any transformations or deformations as they will be ignored.
- (Not yet implemented) In the properties window under the "Scene" context, make any MaMoKo-Scene-related changes.
- Click File > Export > MaMoKo Scene to save the scene.yaml.
- (Not yet implemented) Click File > Export > MaMoKo Experiment Configuration to save the config.yaml.
