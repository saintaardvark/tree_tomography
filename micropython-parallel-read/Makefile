SHELL=/bin/bash

DEV?=/dev/ttyACM0
RSHELL=rshell --port $(DEV)
MODEM_SPEED=115200

.PHONY: install
install:
	$(RSHELL) rsync --mirror . /pyboard

log:
	source ../.venv/bin/activate && ./logger.py
