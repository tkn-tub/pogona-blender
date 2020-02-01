blender_home_dirs := $(shell find ~/.config/blender/ -mindepth 1 -maxdepth 1 -type d)  # -print0 | sort -rz)
blender_latest_home_dir := $(lastword ${blender_home_dirs})

.PHONY:
all: pogona.zip

pogona.zip:
	rm -rf addons/pogona/__pycache__
	cd addons/pogona && zip -r ../../$@ ./

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
	@# echo Selecting the following for installation: ${blender_latest_home_dir}
	@echo

	# mkdir -p ${blender_latest_home_dir}/scripts/addons
	# ln -s $(realpath ./addons/pogona) \
	#    	${blender_latest_home_dir}/scripts/addons/pogona
	for blender_home_dir in ${blender_home_dirs}; do \
		echo Adding to $${blender_home_dir}; \
		mkdir -p $${blender_home_dir}/scripts/addons; \
		ln -sf $(realpath ./addons/pogona) $${blender_home_dir}/scripts/addons/pogona; \
	done

.PHONY:
clean:
	rm -f pogona.zip
