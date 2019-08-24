blender_home_dirs := $(shell find ~/.config/blender/ -mindepth 1 -maxdepth 1 -type d)
blender_latest_home_dir := $(lastword ${blender_home_dirs})

.PHONY:
all: mamoko.zip

mamoko.zip:
	cd addons/mamoko && zip -r ../../$@ ./

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
