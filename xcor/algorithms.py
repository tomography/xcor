#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import logging
import warnings

logger = logging.getLogger(__name__)


__author__ = "Doga Gursoy"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['align']


def align(prj, ang, iters=10, pad=False):
    """Aligns the projection image stack using the conventional
    re-projection algorithm.

    Parameters
    ----------
    prj : ndarray
        3D stack of projection images. The first dimension
        is projection axis, second and third dimensions are
        the x- and y-axes of the projection image, respectively.
    ang : ndarray 
        Projection angles in radians as an array.
    iters : scalar, optional
        Number of iterations of the algorithm.
    pad : bool
        Determines if the projection image width 
        should be padded or not. If true, then the diagonal
        length of the object size is used as the width of 
        the projection image width.

    Returns
    -------
    ndarray
        3D stack of projection images with jitter.
    ndarray
        Error array for each iteration.
    """
    
    from xcor.utils import scale 
    from skimage import transform as tf
    from skimage.feature import register_translation
    import tomopy

    # Needs scaling for skimage float operations.
    prj, scl = scale(prj)

    # Register each image frame-by-frame.
    for n in range(iters):

        print(n)

        # Reconstruct image.
        rec = tomopy.recon(prj, ang, algorithm='gridrec')

        # Re-project data and obtain simulated data.
        sim = tomopy.project(rec, ang, pad)

        # Initialize error matrix per iteration.
        err = np.zeros((iters, prj.shape[0]))

        # For each projection
        for m in range(prj.shape[0]):

            # Register current projection in sub-pixel precision
            shift, error, diffphase = register_translation(prj[m], sim[m], 100)
            err[n, m] = np.sqrt(shift[0]*shift[0] + shift[1]*shift[1])

            # Register current image with the simulated one
            tform = tf.SimilarityTransform(translation=(shift[1], shift[0]))
            prj[m] = tf.warp(prj[m], tform, order=5)

    # Re-normalize data
    prj *= scl
    return prj, np.linalg.norm(err)