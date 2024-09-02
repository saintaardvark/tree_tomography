SHELL=/bin/bash

DEV?=/dev/ttyACM0
RSHELL=rshell --port $(DEV)
MODEM_SPEED=115200

.PHONY: install
install:
	$(RSHELL) rsync --mirror firmware/. /pyboard

log:
	source ../.venv/bin/activate && ./logger.py

plog:
	source ../.venv/bin/activate && ./live_logger.py
