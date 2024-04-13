"""
===============
Embedding in Tk
===============

"""

import tkinter

import numpy as np
import matplotlib.pyplot as plt

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from PIL import Image, ImageTk

root = tkinter.Tk()
root.wm_title("RC Snubber")

Fring = 8.3e6 ## Noise Frequency
Ftest = 6.4e6 ## New Noise Frequency after adding Ctest
# ~ Ctest = 0.5e-9
Ctest = 1.69e-9
Vs = 20 ## Supply Voltage
Fs = 8e3 ## Switching Frequency

CP = Ctest/(np.power((Fring/Ftest),2) - 1) ## Parasitic Capacitance
LP = 1/(CP*(np.power(2*np.pi*Fring,2))) ## Parasitic Inductance
# ~ DF = 0.25
DF = 0.125	## Damping Factor
# ~ RS = (1/(2*DF)) * np.sqrt(LP/CP)
RS = (DF/(2) * np.sqrt(LP/CP))	## Snubber Resistor
CS = 1/(2*np.pi*RS*Fring)	## Snubber Capacitor
Pdiss = CS*np.power(Vs,2)*Fs	## Power dissipated in snubbing resistor

def rc(t, rs):
    return (np.exp(-t * rs) * np.sin(2*np.pi*t))

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02) 

# ~ plt.figure()
# ~ plt.subplot(211)
# ~ plt.plot(t1, rc(t1, RS), 'go', t2, rc(t2, RS), 'k')


fig = Figure(figsize=(10, 4), dpi=100)
t = np.arange(0, 5, .01) ## start, stop, step
ax = fig.add_subplot()
# ~ line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
# ~ line, = plt.plot(t1, rc(t1, RS), 'go', t2, rc(t2, RS), 'k')
line, = ax.plot(t1, rc(t1, RS), 'g')
ax.set_autoscaley_on(True)
ax.set_xlabel("time [nS]")
ax.set_ylabel("f(t)")
# ~ plt.ylim(-3,3)
# ~ plt.ylim(-3,3)
# ~ plt.figure().set_figheight(5)
# ~ plt.subplots_adjust(bottom=0.5)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)


def update_frequency(new_val):
    # retrieve frequency
    f = float(new_val)

    # update data
    y = 2 * np.sin(2 * np.pi * f * t)
    line.set_data(t, y)

    # required to update canvas and attached toolbar!
    canvas.draw()


def update_data(damp_fact):
    # retrieve frequency
    d = float(damp_fact)

    # update data
    y = np.exp(-t * RS * d) * np.sin(2*np.pi*t)
    line.set_data(t, y)

    # required to update canvas and attached toolbar!
    canvas.draw()


slider_update = tkinter.Scale(root, from_=-1, to=16, orient=tkinter.HORIZONTAL,
                              command=update_data, label="Damp Factor")

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.

button_quit.pack(side=tkinter.BOTTOM)
slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
tkinter.mainloop()
