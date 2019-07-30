# MAKEFILE
#
# @link        https://github.com/tecnickcom/unitmulti
# ------------------------------------------------------------------------------

# Use bash as shell (Note: Ubuntu now uses dash which doesn't support PIPESTATUS).
SHELL=/bin/bash

# CVS path (path to the parent dir containing the project)
CVSPATH=github.com/tecnickcom

# Project owner
OWNER=Tecnick.com LTD

# Project vendor
VENDOR=tecnickcom

# Project name
PROJECT=unitmulti

# Project version
VERSION=$(shell cat VERSION)

# Project release number (packaging build number)
RELEASE=$(shell cat RELEASE)

# Name of RPM or DEB package
PKGNAME=${VENDOR}-${PROJECT}

# Current directory
CURRENTDIR=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))

# Conda environment
CONDA_ENV=$(shell dirname ${CURRENTDIR})/env-${PROJECT}

# Include default build configuration
include $(CURRENTDIR)/config.mk

# extract all packages
ALLPACKAGES=$(shell cat conda/meta.yaml | grep -oP '^\s*-\s\K(.*)' | sed "s/.*${PROJECT}//" | sed '/^\s*$$/d' | sort -u | tr -d ' ' | sed 's/[^ ][^ ]*/"&"/g' | tr '\r\n' ' ')


# --- MAKE TARGETS ---

# Display general help about this command
.PHONY: help
help:
	@echo ""
	@echo "$(PROJECT) Makefile."
	@echo "The following commands are available:"
	@echo ""
	@echo "    make version    : Set version from VERSION file"
	@echo "    make conda      : Build minimal Conda environment"
	@echo "    make conda_dev  : Build development Conda environment"
	@echo "    make build      : Build a Conda package"
	@echo "    make wheel      : Build a Wheel package"
	@echo "    make vtest      : Execute tests inside a Python 2.7 virtualenv"
	@echo "    make dbuild     : Build everything inside a Docker container"
	@echo "    make test       : Execute test command - you shuould activate the conda_dev environment first"
	@echo "    make lint       : Evaluate code"
	@echo "    make doc        : Start a server to display source code documentation"
	@echo "    make format     : Format the source code"
	@echo "    make clean      : Remove any build artifact"
	@echo ""

all: help

# Set the version from VERSION file
.PHONY: version
version:
	sed -i "s/version:.*$$/version: $(VERSION)/" conda/meta.yaml
	sed -i "s/number:.*$$/number: $(RELEASE)/" conda/meta.yaml
	sed -i "s/__version__.*$$/__version__ = '$(VERSION)'/" unitmulti/__init__.py
	sed -i "s/__release__.*$$/__release__ = '$(RELEASE)'/" unitmulti/__init__.py

# Build minimal Conda environment
.PHONY: conda
conda:
	./conda/setup-conda.sh

# Build development Conda environment
.PHONY: conda_dev
conda_dev:
	ENV_NAME=env-dev-unitmulti ./conda/setup-conda.sh
	. ../env-dev-unitmulti/bin/activate && \
	../env-dev-unitmulti/bin/conda install --override-channels $(CONDA_CHANNELS) -y $(ALLPACKAGES)

# Build a conda package
.PHONY: build
build: clean version conda
	mkdir -p target
	PROJECT_ROOT=${CURRENTDIR} "${CONDA_ENV}/bin/conda" build --prefix-length 128 --no-anaconda-upload --override-channels $(CONDA_CHANNELS) conda

# Build a Wheel package
.PHONY: wheel
wheel: clean version
	python setup.py sdist bdist_wheel

# Test the project in a Python 2.7 virtual environment
.PHONY: vtest
vtest:
	rm -rf venv
	virtualenv -p /usr/bin/python2.7 venv
	source venv/bin/activate && pip install -e .[test] && make test && coverage html

# Test using setuptools
.PHONY: test
test:
	python setup.py test

# Evaluate code
.PHONY: lint
lint:
	pyflakes ${PROJECT}
	pylint ${PROJECT}
	pycodestyle --max-line-length=120 ${PROJECT}

# Generate source code documentation
.PHONY: doc
doc:
	pydoc -p 1234 $(PROJECT)

# Format the source code
.PHONY: format
format:
	find . -path ./venv -prune -o -path ./target -prune -o -type f -name '*.py' -exec autopep8 --in-place --max-line-length=255 {} \;

# Remove any build artifact
.PHONY: clean
clean:
	rm -rf venv target Dockerfile htmlcov build dist .pytest_cache .cache .benchmarks ./test/*.so ./test/__pycache__ ./unitmulti/__pycache__ ./unitmulti.egg-info
	find . -type f -name '*.pyc' -exec rm -f {} \;

# Build everything inside a Docker container
.PHONY: dbuild
dbuild:
	@mkdir -p target
	@rm -rf target/*
	@echo 0 > target/make.exit
	CVSPATH=$(CVSPATH) VENDOR=$(VENDOR) PROJECT=$(PROJECT) MAKETARGET='$(MAKETARGET)' ./dockerbuild.sh
	@exit `cat target/make.exit`
