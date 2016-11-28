#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import pkg_resources
    __version__ = pkg_resources.working_set.require("tomopy")[0].version
except:
    pass

from xcor.algorithms import *
from xcor.plot import *
from xcor.simulate import *
