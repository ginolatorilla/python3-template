'''
Copyright (c) 2019 Gino Latorilla.
'''

import pytest
from .testables import yourproject


def test_yourfunction():
    assert(0 == yourproject.submodule.yourfunction())
