# Gino's Python with pipenv project template

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/python-linux?label=ubuntu-latest&style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/python-windows?label=windows-latest&style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/python-macos?label=macos-latest&style=plastic)

A Python3 project template with pipenv to hande dependencies.

Inspired by [Kenneth Reitz's project template](https://github.com/kennethreitz/samplemod).

## Features

- Support for Python 3.6, 3.7, and 3.8
- Support for Linux, Windows, and MacOS
- GitHub workflow templates
- Linting with `pycodestyle` (formerly `pep8`)
- Test-driven development with PyTest
- Support for Pipenv with localised `virtualenv` directory

## Requirements

- Python 3.6 or better
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)

## Quick Start

```bash
./bootstrap.py
pipenv run pycodestyle
pipenv run pytest
```

Make sure to rename the following files and directories

- `yourproject/**`
- `tests/yourproject_test.py`

Add modules to be tested in `tests/testables.py`
