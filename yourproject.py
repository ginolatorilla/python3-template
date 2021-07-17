#!/usr/bin/env python3

"""
Describe in this sentence what this program does.

Copyright (c) 2019 Gino Latorilla. All rights reserved.
"""

import argparse
import submodule.main


def main():
    program_options = get_program_options()
    x = submodule.main.yourfunction()
    # Continue here

    return x


def get_program_options():
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args()


if __name__ == '__main__':
    main()
