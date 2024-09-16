PV ?= pulseview-NIGHTLY-x86_64-debug.appimage
SR ?= sigrok-cli-NIGHTLY-x86_64-debug.appimage


log:
	./logger.py

console:
	screen /dev/ttyACM0 921600

pv:
	$(PV) -i foo.csv -I csv:header=yes:column_formats='*b':samplerate=10000000

check:
	$(MAKE) sr | head
sr:
	$(SR) -i foo.csv -I csv:header=yes:column_formats='*b':samplerate=10000000
