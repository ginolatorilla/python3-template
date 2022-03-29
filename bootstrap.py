#!/usr/bin/env python3
"""
Copyright (c) 2022 Gino Latorilla. All rights reserved.
"""

import argparse
import logging
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import Field, dataclass, field, fields
from pathlib import Path
from string import Template
from tempfile import mkdtemp
from typing import Any, Tuple, Type

APP_NAME = Path(sys.argv[0]).stem
log = logging.getLogger(APP_NAME)


def main() -> int:
    program_options = ProgramOptions.parse_args()
    setup_logger(program_options.verbosity)

    if not program_options.project.isidentifier():
        log.error(f'{program_options.project} is not a valid Python identifier.')
        return 1

    new_project_root = Path(program_options.destination) / program_options.project
    if new_project_root.exists():
        log.error(f'The project destination directory exists: {new_project_root}.')
        return 1

    staging_directory = Path(mkdtemp())
    log.debug(f'We have created a temporary staging directory here: {staging_directory}')

    log.debug(f'Copying project tree to: {staging_directory}')
    shutil.copytree(src=Path(__file__).parent, dst=staging_directory, dirs_exist_ok=True)

    log.debug('Removing files that are ignored or not tracked by Git.')
    subprocess.run(shlex.split(f'git -C "{staging_directory}" clean -ffxd'), stdout=subprocess.DEVNULL)

    log.debug('Removing files that are used by Git.')
    for path in staging_directory.glob('.git'):
        path.unlink() if path.is_file() else shutil.rmtree(path)

    log.debug('Removing the copy of this bootstrapping script.')
    (staging_directory / 'bootstrap.py').unlink()

    if program_options.layout == 'module':
        log.debug('Removing the package directory because you chose "module" as the project layout.')
        shutil.rmtree(staging_directory / 'submodule')

        log.debug(f'Renaming the module to {program_options.project}.py.')
        (staging_directory / 'yourproject.py').rename(staging_directory / f'{program_options.project}.py')
    else:
        log.debug('Removing the module file because you chose "package" as the project layout.')
        (staging_directory / 'yourproject.py').unlink()

        log.debug(f'Renaming the package directory to {program_options.project}/.')
        (staging_directory / 'submodule').rename(staging_directory / f'{program_options.project}')

    log.debug('Substituting project name in setup.cfg.')
    with open(staging_directory / 'setup.cfg', 'r+') as fp:
        setup_config_template = Template(fp.read())
        fp.seek(0)
        fp.write(setup_config_template.safe_substitute(project_name=program_options.project))
        fp.truncate()

    log.debug(f'Moving staging directory to destination: {new_project_root}')
    new_project_root.mkdir(parents=True, exist_ok=True)
    staging_directory.rename(new_project_root)

    log.debug('Creating virtual environment with Pipenv.')
    env = os.environ.copy()
    env['PIPENV_VENV_IN_PROJECT'] = '1'
    subprocess.run(shlex.split('pipenv --python 3 --three'), env=env, cwd=new_project_root)
    subprocess.run(shlex.split('pipenv uninstall yourproject'), env=env, cwd=new_project_root)
    if program_options.colour:
        subprocess.run(shlex.split('pipenv install --editable .[pretty] --dev'), env=env, cwd=new_project_root)
    else:
        subprocess.run(shlex.split('pipenv install --editable . --dev'), env=env, cwd=new_project_root)

    log.debug('Running all tests.')
    subprocess.run(shlex.split('pipenv run mypy .'), env=env, cwd=new_project_root)
    subprocess.run(shlex.split('pipenv run flake8'), env=env, cwd=new_project_root)
    subprocess.run(shlex.split('pipenv run pytest --cov-report=term'), env=env, cwd=new_project_root)

    log.debug('Re-initialising Git repository')
    subprocess.run(shlex.split(f'git -C {new_project_root} init'))
    return 0


@dataclass
class ProgramOptions:
    project: str = field(metadata={
        'positional': True,
        'add_argument_kwargs': {
            'help': 'The name of your project.'
        },
    })

    destination: str = field(
        metadata={
            'flags': {'-d'},
            'add_argument_kwargs': {
                'help': 'Create project root in this directory. ',
                'default': str(Path('.').absolute()),
            }
        })

    verbosity: int = field(
        metadata={
            'flags': {'-v'},
            'add_argument_kwargs': {
                'help': 'Increase logging verbosity. Can be specified multiple times.',
                'action': 'count',
                'default': 0,
                'dest': 'verbosity'
            }
        })

    layout: str = field(
        metadata={
            'add_argument_kwargs': {
                'help': '"module": The project will be a single Python module. '
                '"package": The project will be a package (a directory with __init__.py)',
                'choices': {'module', 'package'},
                'default': 'module'
            }
        })

    colour: str = field(
        metadata={
            'flags': {'-c', '--color'},
            'add_argument_kwargs': {
                'help': 'Enable rich text formatting support in the cli.'
                '"package": The project will be a package (a directory with __init__.py)',
                'action': 'store_true',
            }
        })

    @classmethod
    def make_cl_argument_parser(cls) -> argparse.ArgumentParser:
        def args_from_field_metadata(field: Field) -> Tuple[Any, ...]:  # type: ignore
            if field.metadata.get('positional'):
                return (field.name, )
            else:
                return (*field.metadata.get('flags', {}), f'--{field.name}')

        arguments_spec = {
            args_from_field_metadata(field): field.metadata['add_argument_kwargs']
            for field in fields(cls)
        }

        ap = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=type('Formatter', (
                                         argparse.RawDescriptionHelpFormatter,
                                         argparse.ArgumentDefaultsHelpFormatter,
                                     ), {}))
        for args, kwargs in arguments_spec.items():
            ap.add_argument(*args, **kwargs)
        return ap

    @classmethod
    def parse_args(cls) -> Type['ProgramOptions']:
        return cls.make_cl_argument_parser().parse_args(namespace=cls)


def setup_logger(verbosity: int) -> None:
    assert verbosity >= 0

    log_levels = {
        0: {
            'global': logging.WARNING,
            'local': logging.INFO
        },
        1: {
            'global': logging.WARNING,
            'local': logging.DEBUG
        },
        2: {
            'global': logging.INFO,
            'local': logging.DEBUG
        },
    }.get(verbosity, {
        'global': logging.DEBUG,
        'local': logging.DEBUG
    })

    log_format = {
        0: '[{levelname}] {name}: {message}',
        1: '[{levelname}] {name}: {message}',
        2: '<{asctime}> [{levelname}] {name}: {message}',
        3: '<{asctime}> [{levelname}] [pid={process}] {name}: {message}',
    }.get(verbosity, '<{asctime}> [{levelname}] [pid={process}] [tid={thread}] {name}({pathname}:{lineno}): {message}')

    logging.basicConfig(level=log_levels['global'], style='{', format=log_format)
    log.setLevel(log_levels['local'])
    log.debug(f'Log level is {verbosity}.')


if __name__ == '__main__':
    sys.exit(main())
