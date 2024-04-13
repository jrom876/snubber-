"""
.. redirect-from:: /tutorials/introductory/pyplot

.. _pyplot_tutorial:

===============
Pyplot tutorial
===============

An introduction to the pyplot interface.  Please also see
:ref:`quick_start` for an overview of how Matplotlib
works and :ref:`api_interfaces` for an explanation of the trade-offs between the
supported user APIs.

"""

# %%
# Introduction to pyplot
# ======================
#
# :mod:`matplotlib.pyplot` is a collection of functions that make matplotlib
# work like MATLAB.  Each ``pyplot`` function makes some change to a figure:
# e.g., creates a figure, creates a plotting area in a figure, plots some lines
# in a plotting area, decorates the plot with labels, etc.
#
# In :mod:`matplotlib.pyplot` various states are preserved
# across function calls, so that it keeps track of things like
# the current figure and plotting area, and the plotting
# functions are directed to the current axes (please note that "axes" here
# and in most places in the documentation refers to the *axes*
# :ref:`part of a figure <figure_parts>`
# and not the strict mathematical term for more than one axis).
#
# .. note::
#
#    The implicit pyplot API is generally less verbose but also not as flexible as the
#    explicit API.  Most of the function calls you see here can also be called
#    as methods from an ``Axes`` object. We recommend browsing the tutorials
#    and examples to see how this works. See :ref:`api_interfaces` for an
#    explanation of the trade-off of the supported user APIs.
#
# Generating visualizations with pyplot is very quick:

import matplotlib.pyplot as plt
import numpy as np

# %%
# .. _controlling-line-properties:
#
# Controlling line properties
# ===========================
#
# Lines have many attributes that you can set: linewidth, dash style,
# antialiased, etc; see `matplotlib.lines.Line2D`.  There are
# several ways to set line properties
#
# * Use keyword arguments::
#
#       plt.plot(x, y, linewidth=2.0)
#
#
# * Use the setter methods of a ``Line2D`` instance.  ``plot`` returns a list
#   of ``Line2D`` objects; e.g., ``line1, line2 = plot(x1, y1, x2, y2)``.  In the code
#   below we will suppose that we have only
#   one line so that the list returned is of length 1.  We use tuple unpacking with
#   ``line,`` to get the first element of that list::
#
#       line, = plt.plot(x, y, '-')
#       line.set_antialiased(False) # turn off antialiasing
#
# * Use `~.pyplot.setp`.  The example below
#   uses a MATLAB-style function to set multiple properties
#   on a list of lines.  ``setp`` works transparently with a list of objects
#   or a single object.  You can either use python keyword arguments or
#   MATLAB-style string/value pairs::
#
#       lines = plt.plot(x1, y1, x2, y2)
#       # use keyword arguments
#       plt.setp(lines, color='r', linewidth=2.0)
#       # or MATLAB style string value pairs
#       plt.setp(lines, 'color', 'r', 'linewidth', 2.0)
#
#
# Here are the available `~.lines.Line2D` properties.
#
# ======================  ==================================================
# Property                Value Type
# ======================  ==================================================
# alpha                   float
# animated                [True | False]
# antialiased or aa       [True | False]
# clip_box                a matplotlib.transform.Bbox instance
# clip_on                 [True | False]
# clip_path               a Path instance and a Transform instance, a Patch
# color or c              any matplotlib color
# contains                the hit testing function
# dash_capstyle           [``'butt'`` | ``'round'`` | ``'projecting'``]
# dash_joinstyle          [``'miter'`` | ``'round'`` | ``'bevel'``]
# dashes                  sequence of on/off ink in points
# data                    (np.array xdata, np.array ydata)
# figure                  a matplotlib.figure.Figure instance
# label                   any string
# linestyle or ls         [ ``'-'`` | ``'--'`` | ``'-.'`` | ``':'`` | ``'steps'`` | ...]
# linewidth or lw         float value in points
# marker                  [ ``'+'`` | ``','`` | ``'.'`` | ``'1'`` | ``'2'`` | ``'3'`` | ``'4'`` ]
# markeredgecolor or mec  any matplotlib color
# markeredgewidth or mew  float value in points
# markerfacecolor or mfc  any matplotlib color
# markersize or ms        float
# markevery               [ None | integer | (startind, stride) ]
# picker                  used in interactive line selection
# pickradius              the line pick selection radius
# solid_capstyle          [``'butt'`` | ``'round'`` | ``'projecting'``]
# solid_joinstyle         [``'miter'`` | ``'round'`` | ``'bevel'``]
# transform               a matplotlib.transforms.Transform instance
# visible                 [True | False]
# xdata                   np.array
# ydata                   np.array
# zorder                  any number
# ======================  ==================================================
#
# To get a list of settable line properties, call the
# `~.pyplot.setp` function with a line or lines as argument
#
# .. sourcecode:: ipython
#
#     In [69]: lines = plt.plot([1, 2, 3])
#
#     In [70]: plt.setp(lines)
#       alpha: float
#       animated: [True | False]
#       antialiased or aa: [True | False]
#       ...snip
#
# .. _multiple-figs-axes:
#
#
# Working with multiple figures and axes
# ======================================
#
# MATLAB, and :mod:`.pyplot`, have the concept of the current figure
# and the current axes.  All plotting functions apply to the current
# axes.  The function `~.pyplot.gca` returns the current axes (a
# `matplotlib.axes.Axes` instance), and `~.pyplot.gcf` returns the current
# figure (a `matplotlib.figure.Figure` instance). Normally, you don't have to
# worry about this, because it is all taken care of behind the scenes.  Below
# is a script to create two subplots.

Fring = 8.3e6 ## Noise Frequency
Ftest = 6.4e6 ## New Noise Frequency after adding Ctest
Ctest = 0.5e-9
# ~ Ctest = 1.69e-9
Vs = 20 ## Supply Voltage
Fs = 8e3 ## Switching Frequency

CP = Ctest/(np.power((Fring/Ftest),2) - 1) ## Parasitic Capacitance
LP = 1/(CP*(np.power(2*np.pi*Fring,2))) ## Parasitic Inductance
# ~ DF = 0.25
DF = 1	## Damping Factor
# ~ RS = (1/(2*DF)) * np.sqrt(LP/CP)
RS = (DF/(2) * np.sqrt(LP/CP))	## Snubber Resistor
CS = 1/(2*np.pi*RS*Fring)	## Snubber Capacitor
Pdiss = CS*np.power(Vs,2)*Fs	## Power dissipated in snubbing resistor

def f(t):
	return np.exp(-t) * np.cos(2*np.pi*t)

def rc(t, rs):
    return (np.exp(-t * rs) * np.cos(2*np.pi*t))

def rlc(t, df):
    return (1/(2*df) * np.sqrt(LP/CP)) * np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.1)
t3 = np.arange(0.0, 5.0, 0.02)
t4 = np.arange(0.0, 5.0, 0.02) 

plt.figure()
plt.subplot(311)
# ~ plt.subplot(411)
plt.plot(t1, rc(t1, RS), 'go', t4, rc(t4, RS), 'k')

plt.subplot(312)
plt.plot(t1, rc(t1, RS/8), 'bo', t4, rc(t4, RS/8), 'k')

plt.subplot(313)
plt.plot(t1, rc(t1, RS/32), 'ro', t4, rc(t4, RS/32), 'k')

# ~ plt.subplot(412)
# ~ plt.plot(t2, f(t2), 'bo', t3, f(t3), 'k')

# ~ plt.subplot(413)
# ~ plt.plot(t3, np.cos(2*np.pi*t3), 'r--')

# ~ plt.subplot(414)
# ~ ### ~ plt.plot(t4, rlc(t4, 0.25), 'ro', t3, rc(t3, 0.25), 'k')
# ~ plt.plot(t4, rlc(t4, DF), 'r--')
# ~ ### ~ plt.plot(t4, np.cos(2*np.pi*t3), 'r--')

plt.show()


# %%
# It is also possible to add your own scale, see `matplotlib.scale` for
# details.
