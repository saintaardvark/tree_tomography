SHELL=bash

PATH_TO_JUPYTER_VENV=~/dev/src/jupyter_scratch/.venv/bin/activate

jl:
	source $(PATH_TO_JUPYTER_VENV) && jupyter-lab --no-browser

include Makefile.venv
