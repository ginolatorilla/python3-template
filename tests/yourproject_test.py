"""
Copyright (c) 2019 Gino Latorilla. All rights reserved.
"""

import pytest
import yourproject
import submodule
import submodule.main


def test_yourproject_main():
    assert yourproject.main() == 0

def test_yourfunction():
    assert submodule.main.yourfunction() == 0
