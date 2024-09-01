SHELL=bash

PATH_TO_JUPYTER_VENV=~/dev/src/jupyter_scratch/.venv/bin/activate

jl:
	source $(PATH_TO_JUPYTER_VENV) && jupyter-lab --no-browser


log: venv
	$(VENV)/python util/logger.py


install:
	cd micropython && $(MAKE) install

install-par:
	cd micropython-parallel-read/ && $(MAKE) install
console:
	screen /dev/ttyACM0 115200

include Makefile.venv
