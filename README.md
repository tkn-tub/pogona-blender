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
After making a change, simply disable and re-enable the add-on.
