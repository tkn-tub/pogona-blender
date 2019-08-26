blender_home_dirs := $(shell find ~/.config/blender/ -mindepth 1 -maxdepth 1 -type d)
blender_latest_home_dir := $(lastword ${blender_home_dirs})

.PHONY:
all: mamoko.zip

mamoko.zip:
	cd addons/mamoko && zip -r ../../$@ ./

.PHONY:
.ONESHELL:
devel-virtualenv:
	@echo "Installing fake-bpy-module into a virtualenv for bpy code completion outside blender"
	@echo "See https://github.com/nutti/fake-bpy-module/ for details"
	virtualenv -p python3 venv
	source venv/bin/activate
	pip install fake-bpy-module-$(shell basename ${blender_latest_home_dir})  # e.g., fake-bpy-module-2.80

.PHONY:
.ONESHELL:
install-devel:
	@echo Found Blender directories in your home directory: ${blender_home_dirs}
	@echo Selecting the following for installation: ${blender_latest_home_dir}
	@echo

	mkdir -p ${blender_latest_home_dir}/scripts/addons
	ln -s $(realpath ./addons/mamoko) \
	   	${blender_latest_home_dir}/scripts/addons/mamoko

.PHONY:
clean:
	rm -f mamoko.zip
