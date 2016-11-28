#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xcor
import numpy as np
import dxchange

# Import discretisized 3D object.
obj = np.load('data/shepp-logan.npy')

# Define projection angles as an array.
ang = np.linspace(0, np.pi, 90)

# Calculate projection images for given angles.
prj = xcor.project(obj, ang, pad=False)

# Add jitter in projections.
prj = xcor.add_jitter(prj, -8, 8)

# Add noise in projections.
prj = xcor.add_noise(prj, 0.01)

# Align projection images.
prj, err = xcor.align(prj, ang, 2, pad=False)
print (prj.shape)

dxchange.write_tiff(prj, 'tmp/data')