.PHONY:
all: mamoko.zip

mamoko.zip:
	cd addons/mamoko && zip -r ../../$@ ./

.PHONY:
clean:
	rm -f mamoko.zip
