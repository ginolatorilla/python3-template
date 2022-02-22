'''This is a test.
If you think there's no need to describe this in detail, just remove this line, or this entire docstring.

Copyright (c) 2021 Your Company's Name, or you
'''

import yourproject
import submodule
import submodule.main


def test_yourproject_main() -> None:
    yourproject.main(1)


def test_yourfunction() -> None:
    assert submodule.main.yourfunction() == 0
