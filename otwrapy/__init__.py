#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
General purpose OpenTURNS python wrapper tools
"""

import os

__author__ = "Felipe Aguirre Martinez"
__copyright__ = "Copyright 2018 Phimeca Engineering"
__version__ = "0.8"
__email__ = "aguirre@phimeca.fr"

base_dir = os.path.dirname(__file__)

from ._otwrapy import *

__all__ = (_otwrapy.__all__)
