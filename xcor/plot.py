#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import logging
import warnings

logger = logging.getLogger(__name__)


__author__ = "Doga Gursoy"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['plot_error']


def plot_error(sx, sy, jitter):
	"""Plots estimated and true jitter parameters.

	Parameters
	----------
	sx : ndarray
	    Horizontal shifts per projection image in pixels.
	sy : ndarray
	    Vertical shifts per projection image in pixels.
	jitter : ndarray
	    True jitter parameters.
	"""

	# Plot stats
	plt.figure(figsize=(12, 8), facecolor='w')
	plt.suptitle("Re-projection algorithm evaluation", fontsize=14)

	plt.subplot(221)
	plt.plot(np.sum(sx, 0), linewidth=2)
	plt.plot(-jitter[:, 1], 'r')
	plt.ylim([-40, 40])
	plt.ylabel('Vertical shift [pixels]')
	plt.xlabel('Projection angle [degrees]')
	plt.legend(['Estimated', 'True'])
	plt.grid('on')

	plt.subplot(222)
	plt.plot(np.sum(sy, 0), linewidth=2)
	plt.plot(-jitter[:, 0], 'r')
	plt.ylim([-40, 40])
	plt.ylabel('Horizontal shift [pixels]')
	plt.xlabel('Projection angle [degrees]')
	plt.legend(['Estimated', 'True'])
	plt.grid('on')

	plt.subplot(223)
	plt.plot(np.sum(sx, 0)+jitter[:, 1], 'g', linewidth=2)
	plt.ylim([2, -2])
	plt.ylabel('Vertical shift difference [pixels]')
	plt.xlabel('Projection angle [degrees]')
	plt.grid('on')

	plt.subplot(224)
	plt.plot(np.sum(sy, 0)+jitter[:, 0], 'g', linewidth=2)
	plt.ylim([-2, 2])
	plt.ylabel('Horizontal shift difference [pixels]')
	plt.xlabel('Projection angle [degrees]')
	plt.grid('on')

	plt.show()