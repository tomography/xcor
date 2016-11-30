#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xcor
import numpy as np
import dxchange
import tomopy


# Import discretisized 3D object.
obj = np.load('/local/dgursoy/Python/xcor/data/shepp-logan.npy')

# Define projection angles as an array.
ang = np.linspace(0, np.pi, 90)

# Calculate projection images for given angles.
prj = tomopy.project(obj, ang)

# Add jitter in projections.
prj = xcor.add_jitter(prj, -10, 10)

# Add noise in projections.
prj = xcor.add_noise(prj, 0.05)

# Align projection images.
prj, err = xcor.align(prj, ang, 20, pad=(0, 0), save=True)
