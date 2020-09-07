.PHONY: clean install data requirements

# init

SHELL=/bin/bash
PROJECT_NAME=datatracker
CONDA_BASE:=$(shell conda info --base)

# install

update-pip:
	pip install -U pip setuptools wheel

install: clean update-pip
	pip install -e .

install-setup: clean update-pip
	python setup.py install

install-reqs:
	pip install -r requirements.txt

install-dev:
	pip install --upgrade --no-deps --force-reinstall -r requirements-dev.txt

freeze-reqs: install-requirements
	pip freeze > requirements.txt

version:
	@python -c 'import datatracker; print(datatracker.__version__)'

lib-version:
	@python -c 'import $(NAME); print($(NAME).__version__)'

hail-version:
	@python -c 'import hail; print(hail.version())'

# clean

clean: clean-py

clean-py: clean-build clean-pyc clean-test

clean-pyc:
	find . -name '*.py[co]' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

# env

create-env:
	conda create --name $(PROJECT_NAME) python=3.7.4 jupyter=1.0.0

remove-env: clean
	( source $(CONDA_BASE)/etc/profile.d/conda.sh && \
		conda deactivate && \
		conda remove --name $(PROJECT_NAME) --all )

install-version:
	versioneer install

# help

help:
	@echo "    install"
	@echo "        Install package in debug mode with requirements.txt"
	@echo "    install-full"
	@echo "        Full install of package into environment."
	@echo "    update-requirements"
	@echo "        Update package requirements."
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    clean"
	@echo "        Remove all artifacts (Python, build, test)."
	@echo "    clean-pyc"
	@echo "        Remove Python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    clean-test"
	@echo "        Remove test artifacts."
	@echo "    create-env"
	@echo "        Create new Conda environment"
	@echo "    remote-env"
	@echo "        Run clean and remove Conda environment."