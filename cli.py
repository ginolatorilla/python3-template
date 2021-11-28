#!/usr/bin/env python3
# TODO: Replace this docstring. The app will render it when you call it with -h or --help.
'''%(prog)s -- This program does this and that.
This program can do this and that, and many many more.
If you think there's no need to describe this in detail, just remove this line and the one before.

Copyright (c) 2021 Your Company's Name, or you
'''
import sys
import logging
import argparse

import yourproject

log = logging.getLogger(sys.argv[0])


def main():
    # TODO: If you want a simple CLI app, use this function.
    # But if you want a CLI app with subcommands that look like 'git', then delete this function
    # and rename the function 'main_with_subcommands' to 'main'.
    parser = make_cl_argument_parser()
    program_options = parser.parse_args()
    setup_logger(program_options.verbosity)

    # TODO: Continue here, and use program_options.
    yourproject.main(program_options.required, optional=program_options.optional)
    return 0


def make_cl_argument_parser():
    # TODO: Add/remove command line arguments in this dictionary.
    # The 'keys' are positional arguments to argparse.ArgumentParser.add_argument and
    # the 'values' are the keyword arguments.
    arguments_spec = {
        ('required',
         ): {
            'help': 'This is a required argument.'
        },
        (
            '-o',
            '--optional',
        ): {
            'help': 'This is an optional argument.',
            'default': 'default-value-for-optional'
        },
        (
            '-f',
            '--flag',
        ): {
            'help': 'This is a flag, an toggleable optional argument.',
            'action': 'store_true'
        },
        (
            '-v',
            '--verbose',
        ): {
            'help': 'Increase logging verbosity. Can be specified multiple times.',
            'action': 'count',
            'default': 0,
            'dest': 'verbosity'
        }
    }

    _ = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=type(
            'Formatter',
            (argparse.RawDescriptionHelpFormatter,
             argparse.ArgumentDefaultsHelpFormatter),
            {}
        )
    )
    for args, kwargs in arguments_spec.items():
        _.add_argument(*args, **kwargs)
    return _


def setup_logger(verbosity):
    assert verbosity >= 0

    log_levels = {
        0: {
            'global': logging.WARNING,
            'local': logging.WARNING
        },
        1: {
            'global': logging.WARNING,
            'local': logging.INFO
        },
        2: {
            'global': logging.WARNING,
            'local': logging.DEBUG
        },
        3: {
            'global': logging.INFO,
            'local': logging.DEBUG
        },
    }.get(verbosity,
          {
              'global': logging.DEBUG,
              'local': logging.DEBUG
          })

    log_format = {
        0: '[{levelname}] {name}: {message}',
        1: '[{levelname}] {name}: {message}',
        2: '<{asctime}> [{levelname}] {name}: {message}',
        3: '<{asctime}> [{levelname}] [pid={process}] {name}: {message}',
    }.get(verbosity,
          '<{asctime}> [{levelname}] [pid={process} [tid={thread}] {name}({pathname}:{lineno}): {message}')

    logging.basicConfig(level=log_levels['global'], style='{', format=log_format)
    log.setLevel(log_levels['local'])
    log.debug(f'Log level is {verbosity}.')


def main_with_subcommands():
    parser = make_cl_subcommand_parser()
    program_options = parser.parse_args()
    if 'verbosity' in program_options:
        setup_logger(program_options.verbosity)

    return program_options.func(program_options)


def make_cl_subcommand_parser():
    # TODO: Add/remove command line arguments in this dictionary.
    # The 'keys' are positional arguments to argparse.ArgumentParser.add_argument and
    # the 'values' are the keyword arguments.
    common_arguments_spec = {
        (
            '-v',
            '--verbose',
        ): {
            'help': 'Increase logging verbosity. Can be specified multiple times.',
            'action': 'count',
            'default': 0,
            'dest': 'verbosity'
        }
    }

    # TODO: Add/remove subcommands here.
    # The 'keys' are positional arguments to argparse.ArgumentParser.add_subparsers and
    # the 'values' are equivalent to argparse.ArgumentParser.add_argument.
    subcommands_spec = {
        'subcommand': {
            'description': 'This subcommand does this.',
            'arguments_spec': {
                ('required',
                 ): {
                    'help': 'This is a required argument.'
                },
                (
                    '-o',
                    '--optional',
                ): {
                    'help': 'This is an optional argument.',
                    'default': 'default-value-for-optional'
                },
                (
                    '-f',
                    '--flag',
                ): {
                    'help': 'This is a flag, an toggleable optional argument.',
                    'action': 'store_true'
                }
            },
            'entry_point': subcommand_main
        }
    }

    root_parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=type(
            'Formatter',
            (argparse.RawDescriptionHelpFormatter,
             argparse.ArgumentDefaultsHelpFormatter),
            {}
        )
    )
    root_parser.set_defaults(func=lambda _: root_parser.print_help())

    subparsers = root_parser.add_subparsers(description='', dest='subcommand')

    for subcommand, spec in subcommands_spec.items():
        _ = subparsers.add_parser(subcommand, description=spec['description'])
        _.set_defaults(func=spec['entry_point'])
        for args, kwargs in {**common_arguments_spec, **spec['arguments_spec']}.items():
            _.add_argument(*args, **kwargs)

    return root_parser


def subcommand_main(options):
    return 0