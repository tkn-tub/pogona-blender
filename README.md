# MaMoKo Blender Add-on

The Blender Add-on for creating and inspecting scenes for our MaMoKo simulator

## Installation

After following the installation instructions below (respective for your use case), make sure to select the 'Objects path' in the add-on preferences!
This path should point to the directory where all MaMoKo simulator objects are defined.
(TODO: We need a common way of defining objects; right now such a folder does not really exist yet.)

### For Users

1. Create a zip file from the `addons/mamoko/` folder.
    An easy way to do this is simply to run `make` in this directory.
2. Open Blender.
3. Navigate to "Edit" > "Preferences…" > "Add-ons", then click "Install…" and select the zip file from step 1.

### For Add-on Developers

There are several options.

1. Define an alternative scripts path in the Blender preferences.
    1. Go to "Edit" > "Preferences…" > "File Paths" and enter the path to this directory.
2. Link the `addons/mamoko/` directory of this cloned repository into a valid Blender add-ons path, e.g., `~/.config/blender/2.80/scripts/addons/` (see https://docs.blender.org/manual/en/latest/advanced/scripting/introduction.html#file-location for other operating systems).

Having used either of these options, the MaMoKo add-on should now appear in the list of available Add-ons in the Blender preferences.
After making a change, simply disable and re-enable the add-on. (This actually only seems to work in the rarest of cases. When in doubt, restart Blender.)

## Basic Workflow

- Open an empty scene in Blender (yes, you will likely delete the default cube just to add another cube soon after – but it'll be a special cube!)
- Add one or more MaMoKo objects: Hit Shift+A (or click on "Add" in the 3D viewport) and select the desired object template from the "MaMoKo" submenu.
- Select an object and adjust its properties in the properties window under the "Object" context in the "MaMoKo" panel. Don't forget to give it a recognizeable name!
- Transform the object as desired. The location, rotation, and scale of the object will be written out to the scene.yaml later on. If the "Same as Shape" checkbox for the representation is checked, do not use edit mode for any transformations or deformations as they will be ignored.
- (Not yet implemented) In the properties window under the "Scene" context, make any MaMoKo-Scene-related changes.
- Click File > Export > MaMoKo Scene to save the scene.yaml.
- (Not yet implemented) Click File > Export > MaMoKo Experiment Configuration to save the config.yaml.
