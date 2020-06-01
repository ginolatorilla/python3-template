"""
Copyright (c) 2019 Gino Latorilla. All rights reserved.
"""

import pytest
from .testables import yourproject


def test_yourfunction():
    assert(0 == yourproject.submodule.yourfunction())
