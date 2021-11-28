'''This module has some stuff in it.
This module can do this and that, and many many more.
If you think there's no need to describe this in detail, just remove this line and the one before.

Copyright (c) 2021 Your Company's Name, or you
'''
import logging
import submodule.main

def main(required, *, optional=None):
    logging.info(f'Hey, I got {required}.')
    if optional:
        logging.info(f'Hey, I also got {optional}.')

    submodule.main.yourfunction()
