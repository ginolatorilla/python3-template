#!/usr/bin/env python3

"""
Copyright (c) 2019 Gino Latorilla. All rights reserved.
"""

import subprocess
import os
import shlex

env = os.environ.copy()
env['PIPENV_VENV_IN_PROJECT'] = '1'
subprocess.run(shlex.split('pipenv --python 3 --three'), env=env)
subprocess.run(shlex.split('pipenv install --editable . --dev'), env=env)
