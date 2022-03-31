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
from pathlib import Path
from string import Template
from tempfile import mkdtemp
from typing import Any, Dict, Tuple

APP_NAME = Path(sys.argv[0]).stem
log = logging.getLogger(APP_NAME)


def main() -> int:
    program_options = make_cl_argument_parser().parse_args()
    setup_logger(program_options.verbosity)

    if program_options.dev:
        local_project_dir = Path(__file__).parent
        log.info(f'Setting up project for development mode ({local_project_dir.absolute()})')
        log.debug('The following command line arguments will be ignored:')
        log.debug('  --project')
        log.debug('  --directory')
        log.debug('  --layout')
        log.debug('  --colour')

        log.debug('Generating setup.cfg.')
        with open(local_project_dir / 'setup.cfg.template', 'r') as fp:
            setup_config_template = Template(fp.read())

        with open(local_project_dir / 'setup.cfg', 'w') as fp:
            fp.write(setup_config_template.safe_substitute(project_name='yourproject'))

        log.info('Re-initialising project directory: virtual environment and Git')

        log.debug('Creating virtual environment with Pipenv.')
        env = os.environ.copy()
        env['PIPENV_VENV_IN_PROJECT'] = '1'
        subprocess.run(shlex.split('pipenv --python 3 --three'), env=env, cwd=local_project_dir)
        subprocess.run(shlex.split('pipenv install --dev'), env=env, cwd=local_project_dir)
        return 0
    else:
        if not program_options.project.isidentifier():
            log.error(f'{program_options.project} is not a valid Python identifier.')
            return 1

        new_project_root = Path(program_options.destination) / program_options.project
        if new_project_root.exists():
            log.error(f'The project destination directory exists: {new_project_root.absolute()}.')
            return 1

        if os.getenv('VIRTUAL_ENV') is not None:
            log.error(
                'Cannot continue while inside an active Virtual Environment. Did you forget to call "deactivate"?')
            return 1

        log.info(f'Preparing new project root directory in: {new_project_root.absolute()}')
        staging_directory = Path(mkdtemp())
        log.debug(f'We have created a temporary staging directory here: {staging_directory.absolute()}')

        log.debug(f'Copying project tree to: {staging_directory.absolute()}')
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

        log.debug('Generating setup.cfg.')
        with open(staging_directory / 'setup.cfg.template', 'r') as fp:
            setup_config_template = Template(fp.read())

        log.debug('Removing setup.cfg.template.')
        (staging_directory / 'setup.cfg.template').unlink()

        with open(staging_directory / 'setup.cfg', 'w') as fp:
            fp.write(setup_config_template.safe_substitute(project_name=program_options.project))

        log.debug('Removing setup.cfg in .gitignore.')
        with open(staging_directory / '.gitignore', 'r+') as fp:
            lines = [line for line in fp if 'setup.cfg' not in line]
            fp.seek(0)
            fp.writelines(lines)
            fp.truncate()

        log.debug(f'Moving staging directory to destination: {new_project_root.absolute()}')
        new_project_root.mkdir(parents=True, exist_ok=True)
        staging_directory.rename(new_project_root)

        log.info('Re-initialising project directory: virtual environment and Git')

        log.debug('Creating virtual environment with Pipenv.')
        env = os.environ.copy()
        env['PIPENV_VENV_IN_PROJECT'] = '1'
        subprocess.run(shlex.split('pipenv --python 3 --three'), env=env, cwd=new_project_root)
        subprocess.run(shlex.split('pipenv uninstall yourproject'), env=env, cwd=new_project_root)
        if program_options.color:
            subprocess.run(shlex.split('pipenv install --editable .[pretty] --dev'), env=env, cwd=new_project_root)
        else:
            subprocess.run(shlex.split('pipenv install --editable . --dev'), env=env, cwd=new_project_root)

        log.debug('Running all tests.')
        subprocess.run(shlex.split('pipenv run mypy .'), env=env, cwd=new_project_root)
        subprocess.run(shlex.split('pipenv run flake8'), env=env, cwd=new_project_root)
        subprocess.run(shlex.split('pipenv run pytest --cov-report=term'), env=env, cwd=new_project_root)

        log.debug('Re-initialising Git repository')
        subprocess.run(shlex.split(f'git -C {new_project_root} init'))

        log.info(f'Congratulations, you may now work in your new project at: {new_project_root.absolute()}')
        log.info('Make sure to do the following afterwards:')
        log.info('  1. Update docstrings in every new *.py file.')
        log.info('  2. Update all "# TODO" bits in setup.cfg.')
        log.info('  3. Change LICENSE, if necessary.')
        log.info('  4. Update the README.md.')
        return 0


def make_cl_argument_parser() -> argparse.ArgumentParser:
    arguments_spec = {
        ('--project', ): {
            'help': 'The name of your project.',
            'default': 'yourproject'
        },
        ('--dev', ): {
            'help': 'Prepares this project for development mode.',
            'action': 'store_true',
        },
        ('-d', '--destination'): {
            'help': 'Create project root in this directory.',
            'default': str(Path('.').absolute()),
        },
        ('-v', '--verbose'): {
            'help': 'Increase logging verbosity. Can be specified multiple times.',
            'action': 'count',
            'default': 0,
            'dest': 'verbosity'
        },
        ('-l', '--layout'): {
            'help': '"module": The project will be a single Python module. '
            '"package": The project will be a package (a directory with __init__.py)',
            'choices': {'module', 'package'},
            'default': 'module'
        },
        ('-c', '--color', '--colour'): {
            'help': 'Enable rich text formatting support in the cli.'
            '"package": The project will be a package (a directory with __init__.py)',
            'action': 'store_true',
        },
    }  # type: Dict[Tuple[str, ...], Any]

    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=type('Formatter',
                             (argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter), {}))
    for args, kwargs in arguments_spec.items():
        ap.add_argument(*args, **kwargs)
    return ap


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
