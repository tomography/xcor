#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import warnings

logger = logging.getLogger(__name__)


__author__ = "Doga Gursoy"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['scale']


def scale(prj):
    """Linearly scales the projection images in the range
    between -1 and 1. 

    Parameters
    ----------
    prj : ndarray
        3D stack of projection images. The first dimension
        is projection axis, second and third dimensions are
        the x- and y-axes of the projection image, respectively.

    Returns
    -------
    ndarray
        Scaled 3D stack of projection images.
    """
    scl = max(abs(prj.max()), abs(prj.min()))
    prj /= scl
    return prj, scl