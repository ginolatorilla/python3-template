# Gino's Python with pipenv project template

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/python-linux?label=ubuntu-latest&style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/python-windows?label=windows-latest&style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ginolatorilla/python3-pipenv-template/python-macos?label=macos-latest&style=plastic)

A Python3 project template with pipenv to hande dependencies.

Inspired by [Kenneth Reitz's project template](https://github.com/kennethreitz/samplemod).

## Features

- Support for Python 3.8 and greater
- Support for Linux, Windows, and MacOS
- GitHub workflow templates
- Linting with `flake8` and `mypy`
- Formatting with `yapf`
- Test-driven development with PyTest, with mocking and code coverage support

## Requirements

- Python 3.8 or better
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)

## Quick Start

```bash
python3 ./bootstrap.py --project your_new_project_name
```

The bootstrapping script will create your new project's root directory. Follow all of the TODOs
embedded in the newly-created files:

- All `*.py` files.
- `pyproject.toml`

Consider changing the project licence with yours, and adjust the licencing metadata in `setup.cfg`.

This project can be installed to your system or virtual environments via `pip install .` or `./setup.py install`.
To know more, see the [setuptools documentation](https://setuptools.readthedocs.io/en/latest/userguide/index.html).

This project supports an optional feature for coloured console outputs with this install command: `pip install .[pretty]`.

Finally, take ownership of this template project and replace this README!

## Maintaining this Project

```shell
./bootstrap --dev
source .venv/bin/activate
```

You may then continue working in the files local to this project.

If you are going to update `pyproject.toml`, make sure to reflect those changes in `pyproject.toml.template`.
