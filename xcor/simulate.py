#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import logging
import warnings

logger = logging.getLogger(__name__)


__author__ = "Doga Gursoy"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['project', 'tilt', 'add_jitter', 'add_noise']


def project(obj, theta, pad=False):
    """Calculate projection images for a given object at 
    different angles.

    Parameters
    ----------
    obj : ndarray
        3D discrete object.
    theta : ndarray
        An array of projection angles in degrees.
    pad : bool
        Determines if the projection image width 
        should be padded or not. If true, then the diagonal
        length of the object size is used as the width of 
        the projection image width.
    
    Returns
    -------
    ndarray
        3D projection data.
    """
    import tomopy
    return tomopy.project(obj, theta, pad)


def tilt(obj, rad=0, phi=0):
    """Tilt object at a given angle from the rotation axis.

    Warning
    -------
    Not implemented yet.

    Parameters
    ----------
    obj : ndarray
        3D discrete object.
    rad : scalar, optional
        Radius in polar cordinates to define tilt angle. 
        The value is between 0 and 1, where 0 means no tilt
        and 1 means a tilt of 90 degrees. The tilt angle 
        can be obtained by arcsin(rad).
    phi : scalar, optional
        Angle in degrees to define tilt direction from the
        rotation axis. 0 degree means rotation in sagittal
        plane and 90 degree means rotation in coronal plane.

    Returns
    -------
    ndarray
        Tilted 3D object.
    """
    pass


def add_jitter(prj, low=0, high=1):
    """Simulates jitter in projection images. The jitter
    is simulated by drawing random samples from a uniform
    distribution over the half-open interval [low, high).

    Parameters
    ----------
    prj : ndarray
        3D stack of projection images. The first dimension
        is projection axis, second and third dimensions are
        the x- and y-axes of the projection image, respectively.
    low : float, optional
        Lower boundary of the output interval. All values
        generated will be greater than or equal to low. The
        default value is 0.
    high : float
        Upper boundary of the output interval. All values
        generated will be less than high. The default value
        is 1.0.

    Returns
    -------
    ndarray
        3D stack of projection images with jitter.
    """
    from xcor.utils import scale
    from skimage import transform as tf

    # Needs scaling for skimage float operations.
    prj, scl = scale(prj)

    # Random jitter parameters are drawn from uniform distribution.
    ind = np.random.uniform(low, high, size=(prj.shape[0], 2))

    for m in range(prj.shape[0]):
        tform = tf.SimilarityTransform(translation=ind[m])
        prj[m] = tf.warp(prj[m], tform, order=0)

    # Re-scale back to original values.
    prj *= scl
    return prj


def add_noise(prj, ratio=0.05):
    """Adds Gaussian noise with zero mean and a given standard 
    deviation as a ratio of the maximum value in data.

    Parameters
    ----------
    prj : ndarray
        3D stack of projection images. The first dimension
        is projection axis, second and third dimensions are
        the x- and y-axes of the projection image, respectively.
    ratio : float, optional
        Ratio of the standard deviation of the Gaussian noise 
        distribution to the maximum value in data.

    Returns
    -------
    ndarray
        3D stack of projection images with added Gaussian noise.
    """
    std = prj.max() * ratio
    noise = np.random.normal(0, std, size=prj.shape)
    return prj + noise.astype('float32')
