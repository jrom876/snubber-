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

import matplotlib.pyplot as plt
import numpy as np

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from PIL import Image, ImageTk

import os
import csv
import sys
import time
import math
import struct
import tkinter as tk
from tkinter import *

#############################################
############### TKINTER SETUP ###############

root = tk.Tk()
root.title("RC Snubber")
# ~ fig, ax = plt.subplots()

# ~ fig = Figure(figsize=(5, 4), dpi=100)
# ~ t = np.arange(0, 5, .01) ## start, stop, step
# ~ ax = fig.add_subplot()
# ~ ### ~ line, = ax.plot(t, rc(t, RS), 'g')
# ~ line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
# ~ ax.set_xlabel("time [s]")
# ~ ax.set_ylabel("f(t)")

# ~ canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# ~ canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
# ~ canvas.draw()

# ~ root.geometry("1000x500")
# ~ root.geometry("1200x750")
# ~ root.geometry("1200x900")
# ~ column_size = 60
# ~ row_size = 25
#############################################
################## GLOBALS ##################
MILLI = 1.0e-3
MICRO = 1.0e-6
NANO = 1.0e-9
PICO = 1.0e-12
KILO = 1.0e3
MEGA = 1.0e6
GIGA = 1.0e9
TERA = 1.0e12

Fring = 8.3e6 ## Noise Frequency
Ftest = 6.4e6 ## New Noise Frequency after adding Ctest
# ~ Ctest = 0.5e-9
Ctest = 1.69e-9
Vs = 20 ## Supply Voltage
Fs = 8e3 ## Switching Frequency

CP = Ctest/(np.power((Fring/Ftest),2) - 1) ## Parasitic Capacitance
LP = 1/(CP*(np.power(2*np.pi*Fring,2))) ## Parasitic Inductance
# ~ CP = round(Ctest/(np.power((Fring/Ftest),2) - 1)*GIGA,8) ## Parasitic Capacitance
# ~ LP = round(1/(CP*(np.power(2*np.pi*Fring,2)))*GIGA, 8) ## Parasitic Inductance
# ~ DF = 0.25
DF = 1	## Damping Factor
# ~ RS = (1/(2*DF)) * np.sqrt(LP/CP)
RS = round((DF/2.0 * np.sqrt((LP/GIGA)/(CP/GIGA))), 6)	## Snubber Resistor
CS = round(1/(2*np.pi*RS*Fring)*GIGA, 8)	## Snubber Capacitor
Pdiss = round((CS*np.power(Vs,2)*Fs)/GIGA,8)	## Power dissipated in snubbing resistor

####################################################
############### Button Declarations ################
gen_data_button = tk.Button(text="Plot RC", command=lambda: plot_rc(), width=13)

button_quit = tk.Button(text="Quit", command=root.destroy, width=13)

recalc_data_button = tk.Button(text="Recalc DATA", command=lambda: recalc_Data(), width=13)

# ~ clear_data_button = tk.Button(text="Clear DATA", command=lambda: clear_Data_Labels(), width=13)

gen_data_button.grid(row=0, column=0)
recalc_data_button.grid(row=3, column=0)
button_quit.grid(row=6, column=0)
# ~ clear_data_button.grid(row=12, column=0)


###############################################
################## Functions ##################  

def rc(t, rs):
    return (np.exp(-t * rs) * np.sin(2*np.pi*t))

# ~ t1 = np.arange(0.0, 5.0, 0.1)
# ~ t2 = np.arange(0.0, 5.0, 0.02) 

# ~ plt.figure()
# ~ plt.subplot(111)
# ~ plt.plot(t1, rc(t1, RS), 'go', t2, rc(t2, RS), 'k')

# ~ plt.show()

def plot_rc ():
	t1 = np.arange(0.0, 5.0, 0.01)
	# ~ t2 = np.arange(0.0, 5.0, 0.02) 

	plt.figure()
	plt.subplot(111)
	plt.plot(t1, rc(t1, float(RSNUB.get())), 'g')
	# ~ plt.plot(t1, rc(t1, float(RSNUB.get())), 'g', t2, rc(t2, float(RSNUB.get())), 'k')

	plt.show()

def recalc_Data():
	
	FRING.set(float(FRING.get()))
	FTEST.set(float(FTEST.get())) 
	# ~ Ctest = 0.5e-9
	CTEST.set(float(CTEST.get()))
	VSUPP.set(float(VSUPP.get())) 
	FSWIT.set(float(FSWIT.get())) 

	CP = float(CTEST.get())/(np.power((float(FRING.get())/float(FTEST.get())),2) - 1) 
	LP = 1/(CP*(np.power(2*np.pi*float(FRING.get()),2))) 
	# ~ CP = round(Ctest/(np.power((Fring/Ftest),2) - 1)*GIGA,8) 
	# ~ LP = round(1/(CP*(np.power(2*np.pi*Fring,2)))*GIGA, 8) 
	DF = float(DFACT.get())
	# ~ DFACT.set(float(DFACT.get()))	
	# ~ RS = (1/(2*DF)) * np.sqrt(LP/CP)
	RS = round((float(DFACT.get()) * np.sqrt((LP/GIGA)/(CP/GIGA))), 6)	
	# ~ RS = round((DF * np.sqrt((LP/GIGA)/(CP/GIGA))), 6)	
	CS = round(1/(2*np.pi*RS*Fring)*GIGA, 8)	
	Pdiss = round((CS*np.power(Vs,2)*Fs)/GIGA,8)	

def update_data(damp_fact):
    # retrieve frequency
    d = float(damp_fact)

    # update data
    y = np.exp(-t * RS * d) * np.sin(2*np.pi*t)
    line.set_data(t, y)

    # required to update canvas and attached toolbar!
    canvas.draw()

fig = Figure(figsize=(8, 4), dpi=100)
t = np.arange(0, 5, .01) ## start, stop, step
ax = fig.add_subplot()
# ~ line, = ax.plot(t, rc(t, RS), 'g')
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")

# ~ t1 = np.arange(0.0, 5.0, 0.1)
# ~ t2 = np.arange(0.0, 5.0, 0.02) 

# ~ plt.figure()
# ~ plt.subplot(111)
# ~ plt.plot(t1, rc(t1, RS), 'go', t2, rc(t2, RS), 'k')

# ~ plt.show()

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

# ~ button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

slider_update = tk.Scale(root, from_=-1, to=16, orient=tk.HORIZONTAL,
                              command=update_data, label="Damp Factor")

# ~ button_quit.pack(side=tk.BOTTOM)
# ~ slider_update.update()
# ~ slider_update.pack(side=tk.BOTTOM)
canvas.get_tk_widget()
################### Functions and Commands ###################


# ~ def gen_data():
    # ~ gen_element_data()
    # ~ MWset.set(round(globals()['MOL_WEIGHT'], 4))
    # ~ Vset.set(globals()['VALENCE'])
    # ~ SWset.set(gen_mEq_per_L(Tset.get(), SVset.get(), MWset.get(), Vset.get()))


# ~ def show_Data_Labels():
    # ~ gen_element_data()
    # ~ MWset.set(round(globals()['MOL_WEIGHT'], 4))
    # ~ Vset.set(globals()['VALENCE'])
    # ~ SWset.set(gen_mEq_per_L(Tset.get(), SVset.get(), MWset.get(), Vset.get()))
    # ~ clear_Data_Labels()
    # ~ Countset.set(int(gen_count(int(Endset.get()) + int(Multset.get()), int(Startset.get())) / int(Multset.get())))
    # ~ # Countset.set(float(gen_count(int(Endset.get()) + float(Multset.get()), int(Startset.get())) / float(Multset.get())))
    # ~ count = int(Countset.get())
    # ~ for i in range(count):
        # ~ T_val_label_text = tk.StringVar()
        # ~ result = gen_target(float(Startset.get()), i * float(Multset.get()))
        # ~ T_val_label_text.set(gen_target(float(Startset.get()), i * float(Multset.get())))
        # ~ T_val_label = tk.Label(root, textvariable=T_val_label_text, width=10)
        # ~ T_val_label.grid(row=1 + i, column=4)

        # ~ SV_val_label_text = tk.StringVar()
        # ~ SV_val_label_text.set(SVset.get())
        # ~ SV_val_label = tk.Label(root, textvariable=SV_val_label_text, width=10)
        # ~ SV_val_label.grid(row=1 + i, column=5)

        # ~ W_val_label_text = tk.StringVar()
        # ~ W_val_label_text.set((gen_mEq_per_L(result, SVset.get(), MWset.get(), Vset.get())))
        # ~ W_val_label = tk.Label(root, textvariable=W_val_label_text, width=10)
        # ~ W_val_label.grid(row=1 + i, column=6)

    # ~ MW_val_label_text.set(MWset.get())
    # ~ El1_in_label_text.set(E1set.get())
    # ~ El2_in_label_text.set(E2set.get())
    # ~ E1_val_label_text.set(globals()[E1set.get()])
    # ~ E2_val_label_text.set(globals()[E2set.get()])

# ~ print("MOL_WEIGHT\t", globals()['MOL_WEIGHT'])
# ~ print("VALENCE\t", globals()['VALENCE'])

####################################################
################ Entry Declarations ################

FRING = tk.StringVar()
FTEST = tk.StringVar()
CTEST = tk.StringVar()
VSUPP = tk.StringVar()
FSWIT = tk.StringVar()
CPARA = tk.StringVar()
LPARA = tk.StringVar()
DFACT = tk.StringVar()
RSNUB = tk.StringVar()
CSNUB = tk.StringVar()
PDISS = tk.StringVar()

FRING_entry = tk.Entry(root, textvariable=FRING, width=14)
FTEST_entry = tk.Entry(root, textvariable=FTEST, width=14)
CTEST_entry = tk.Entry(root, textvariable=CTEST, width=14)
VSUPP_entry = tk.Entry(root, textvariable=VSUPP, width=14)
FSWIT_entry = tk.Entry(root, textvariable=FSWIT, width=14)
CPARA_entry = tk.Entry(root, textvariable=CPARA, width=14)
LPARA_entry = tk.Entry(root, textvariable=LPARA, width=14)
DFACT_entry = tk.Entry(root, textvariable=DFACT, width=14)
RSNUB_entry = tk.Entry(root, textvariable=RSNUB, width=14)
CSNUB_entry = tk.Entry(root, textvariable=CSNUB, width=14)
PDISS_entry = tk.Entry(root, textvariable=PDISS, width=14)
# ~ E1set_entry = tk.Entry(root, textvariable=E1set, width=14)
# ~ E2set_entry = tk.Entry(root, textvariable=E2set, width=14)

FRING.set(Fring)
FTEST.set(Ftest)
CTEST.set(Ctest)
VSUPP.set(Vs)
FSWIT.set(Fs)
CPARA.set(CP)
LPARA.set(LP)
DFACT.set(DF)
RSNUB.set(RS)
# ~ RSNUB.set(round((float(DFACT.get())/(2) * np.sqrt((float(LPARA.get())/GIGA)/(float(CPARA.get())/GIGA)))*KILO, 6))
CSNUB.set(CS)
PDISS.set(Pdiss)

FRING_entry.grid(row=0,  column=1)
FTEST_entry.grid(row=1,  column=1)
CTEST_entry.grid(row=2,  column=1)
VSUPP_entry.grid(row=3,  column=1)
FSWIT_entry.grid(row=4,  column=1)
CPARA_entry.grid(row=5,  column=1)
LPARA_entry.grid(row=6,  column=1)
DFACT_entry.grid(row=7,  column=1)
RSNUB_entry.grid(row=8,  column=1)
CSNUB_entry.grid(row=9,  column=1)
PDISS_entry.grid(row=10,  column=1)

####################################
########## Create Labels ##########

FRING_label   	= tk.Label(root, text="FRING")
FTEST_label   	= tk.Label(root, text="FTEST")
CTEST_label   	= tk.Label(root, text="CTEST")
VSUPP_label 	= tk.Label(root, text="VSUPP")
FSWIT_label   	= tk.Label(root, text="VSWITCH")
CPARA_label 	= tk.Label(root, text="CPARA")
LPARA_label   	= tk.Label(root, text="LPARA")
DFACT_label 	= tk.Label(root, text="DFACT")
RSNUB_label   	= tk.Label(root, text="RSNUB")
CSNUB_label 	= tk.Label(root, text="CSNUB")
PDISS_label		= tk.Label(root, text="PDISS")

FRING_label = tk.StringVar()
FRING_label_text = tk.StringVar()
FRING_label_text.set("FRING")
FRING_label = tk.Label(root, textvariable=FRING_label_text, width=12)
FRING_label.grid(row=0, column=2)

FTEST_label = tk.StringVar()
FTEST_label_text = tk.StringVar()
FTEST_label_text.set("FTEST")
FTEST_label = tk.Label(root, textvariable=FTEST_label_text, width=12)
FTEST_label.grid(row=1, column=2)

CTEST_label = tk.StringVar()
CTEST_label_text = tk.StringVar()
CTEST_label_text.set("CTEST")
CTEST_label = tk.Label(root, textvariable=CTEST_label_text, width=12)
CTEST_label.grid(row=2, column=2)

VSUPP_label = tk.StringVar()
VSUPP_label_text = tk.StringVar()
VSUPP_label_text.set("V Supply")
VSUPP_label = tk.Label(root, textvariable=VSUPP_label_text, width=12)
VSUPP_label.grid(row=3, column=2)

FSWIT_label = tk.StringVar()
FSWIT_label_text = tk.StringVar()
FSWIT_label_text.set("V Switch")
FSWIT_label = tk.Label(root, textvariable=FSWIT_label_text, width=10)
FSWIT_label.grid(row=4, column=2)

CPARA_label = tk.StringVar()
CPARA_label_text = tk.StringVar()
CPARA_label_text.set("CPARA pF")
CPARA_label = tk.Label(root, textvariable=CPARA_label_text, width=10)
CPARA_label.grid(row=5, column=2)

LPARA_label = tk.StringVar()
LPARA_label_text = tk.StringVar()
LPARA_label_text.set("LPARA pH")
LPARA_label = tk.Label(root, textvariable=LPARA_label_text, width=14)
LPARA_label.grid(row=6, column=2)

DFACT_label = tk.StringVar()
DFACT_label_text = tk.StringVar()
DFACT_label_text.set("Damp Factor")
DFACT_label = tk.Label(root, textvariable=DFACT_label_text, width=14)
DFACT_label.grid(row=7, column=2)

RSNUB_label = tk.StringVar()
RSNUB_label_text = tk.StringVar()
RSNUB_label_text.set("RES SNUB Ohms")
RSNUB_label = tk.Label(root, textvariable=RSNUB_label_text, width=14)
RSNUB_label.grid(row=8, column=2)

CSNUB_label = tk.StringVar()
CSNUB_label_text = tk.StringVar()
CSNUB_label_text.set("CAP SNUB pF")
CSNUB_label = tk.Label(root, textvariable=CSNUB_label_text, width=14)
CSNUB_label.grid(row=9, column=2)

PDISS_label = tk.StringVar()
PDISS_label_text = tk.StringVar()
PDISS_label_text.set("PDISS W")
PDISS_label = tk.Label(root, textvariable=PDISS_label_text, width=10)
PDISS_label.grid(row=10, column=2)


#####################################################
################ The Label Generator ################
# ~ for a in range(30):
	# ~ root.grid_columnconfigure(a,  minsize=column_size)
	# ~ root.grid_rowconfigure(a,  minsize=row_size)
	# ~ FRING_label.grid(   row=0, column=4)
	# ~ FTEST_label.grid(  row=0, column=5)
	# ~ CTEST_label.grid(   row=0, column=6)
	# ~ MWeight_in_label.grid( 	row=0, column=7)
	# ~ El1_in_label.grid( 		row=0, column=8)
	# ~ El2_in_label.grid( 		row=0, column=9)

root.update()
root.mainloop()

