# Gino's Python with pipenv project template

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/Python%20application)

A Python3 project template with pipenv to hande dependencies.

Inspired by [Kenneth Reitz's project template](https://github.com/kennethreitz/samplemod).

## Features

- Support for Python 3.6
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
