"""
Copyright (c) 2019 Gino Latorilla. All rights reserved.
"""

import sys
import os
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add after this line the modules to be tested
import yourproject.submodule  # noqa: E402
