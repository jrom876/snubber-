#!/usr/bin/python3

# PROJECT		meqcalc
# FILE			testgui.py
# DESIGNER		Jacob Romero 

'''
	Copyright (C) 3/14/2024 
	Jacob Romero, ERI Group, LLC
	jromero@erigroup.com

	References:	
		https://sciencing.com/calculate-milliequivalent-5009675.html
		https://ptable.com/?lang=en#Properties
		https://www.environmentalexpress.com/ee/s/product/detail/01t4W00000EmE1OQAV

	mEq = (mass of solute (mg) * valence) / Molecular Weight of solute
	mEq/L = [(mass of solute (mg) * valence) / Molecular Weight of solute] / volume of solvent (L)
'''

#################################
####### IMPORT STATEMENTS #######
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
root.title("mEq/L Calculator Version 0.0.1")
# ~ root.geometry("1000x500")
# ~ root.geometry("1200x750")
root.geometry("1200x900")
column_size = 60
row_size = 25
#############################################
################## GLOBALS ##################

MOL_WEIGHT 	= 0
VALENCE 	= 0
TVALENCE 	= 0

## Lists of Molecular Weights and Valences of Elements
H	= [1.008, 1]
He 	= [4.026, 2]
Li	= [6.94, 1]
Be 	= [9.012, 2]
B	= [10.81, 3]
C	= [12.011, 4]
N	= [14.077, 3]
O	= [15.999, 2]
F	= [18.998, 1]
Ne	= [20.180, 8]
Na	= [22.99, 1]
Mg 	= [24.305, 2]
Al	= [26.982, 3]
Si	= [28.085, 4]
P 	= [30.974, 3]
S	= [32.06, 2]
Cl	= [35.45, 1]
Ar	= [39.948, 8]
K	= [39.098, 1]
Ca	= [40.078, 2]

####################################################
############### Button Declarations ################
gen_data_button = tk.Button(text="Gen DATA",
		command=lambda: gen_data(), width=13)
                    
show_data_button = tk.Button(text="Show DATA",   
		command=lambda: show_Data_Labels(), width=13)                     
                    
clear_data_button = tk.Button(text="Clear DATA",   
		command=lambda: clear_Data_Labels(), width=13)                     

gen_data_button.grid(row=0,  column=0)
show_data_button.grid(row=10,  column=0)
clear_data_button.grid(row=14,  column=0)

################### Functions and Commands ################### 

def gen_mEq_per_L(target, solV, molWeight, valence):
	mEq = (float(target)*float(solV)*float(molWeight))/int(valence)
	mEq = round(mEq, 4)
	return mEq

def gen_count(end, start):
	count = (int(end) - int(start))
	return int(count)

def gen_target(value, inc):
	meql = (float(value) + float(inc))
	return float(meql)

def gen_data():
	gen_compound(globals()[E1set.get()], globals()[E2set.get()])
	MWset.set(round(globals()['MOL_WEIGHT'], 4))
	Vset.set(globals()['VALENCE'])
	SWset.set(gen_mEq_per_L(Tset.get(), SVset.get(), MWset.get(), Vset.get()))

def gen_compound (element1, element2): 
	globals()['MOL_WEIGHT'] = 0
	globals()['VALENCE'] = 0
	globals()['TVALENCE'] = 0
	el1 = list(element1)
	el2 = list(element2)
	globals()['TVALENCE'] += (el1[1] + el2[1])
	TVset.set(globals()['TVALENCE'])
	if (el1[0] == el2[0]):
		sys.exit("Matching Elements are not allowed")
	
	if ((el1[1] != el2[1]) and ((el1[1]%2 == 0) and (el2[1]%2 == 0))):
		globals()['MOL_WEIGHT'] += ((math.ceil((el1[1])/2)) + (math.ceil((el2[1])/2)))
		print("el1[1]\t", (math.ceil((el1[1])/2)))
		print("el2[1]\t", (math.ceil((el2[1])/2)))
		print("el1[1] + el2[1]\t", (math.ceil((el1[1])/2)) + (math.ceil((el2[1])/2)))
		print("MOL_WEIGHT\t", globals()['MOL_WEIGHT'])
		
	if (el1[1] == 1):
		globals()['MOL_WEIGHT'] += el2[0]	
	elif (el1[1] > 1):
		el2[0] = el1[1] * el2[0]
		globals()['MOL_WEIGHT'] += el2[0]		
	if (el2[1] == 1):
		globals()['MOL_WEIGHT'] += el1[0]	
	elif (el2[1] > 1):
		el1[0] = el2[1] * el1[0]
		globals()['MOL_WEIGHT'] += el1[0]
	
	if (el1[1] == el2[1]):
		el1 = list(element1)
		el2 = list(element2)
		# ~ print("MOL_WEIGHT\t", globals()['MOL_WEIGHT'])
		globals()['MOL_WEIGHT'] = 0
		# ~ print("MOL_WEIGHT\t", globals()['MOL_WEIGHT'])
		globals()['MOL_WEIGHT'] += (el1[0] + el2[0])
		# ~ print("el1[0]\t", el1[0])
		# ~ print("el2[0]\t", el2[0])
		# ~ print("el1[0] + el2[0]\t", el1[0] + el2[0])
		# ~ print("MOL_WEIGHT\t", globals()['MOL_WEIGHT'])

	if ((el1[1] != el2[1]) and ((el1[1]%2 == 0) and (el2[1]%2 == 0))):
		globals()['VALENCE'] += ((math.ceil((el1[1])/2)) + (math.ceil((el2[1])/2)))
		print("el1[1]\t", (math.ceil((el1[1])/2)))
		print("el2[1]\t", (math.ceil((el2[1])/2)))
		print("el1[1] + el2[1]\t", (math.ceil((el1[1])/2)) + (math.ceil((el2[1])/2)))
		print("VALENCE\t", globals()['VALENCE'])
	elif (el1[1] != el2[1]):
		globals()['VALENCE'] += (el1[1] + el2[1])
	elif (el1[1] == el2[1]):
		globals()['VALENCE'] += 2
		
	if (el1[1] == el2[1]):
		Compset.set(E1set.get() + E2set.get())
	elif ((el1[1] == 1) and (el2[1] > 1)):
		Compset.set(E1set.get() + str(el2[1]) + E2set.get())
	elif ((el1[1] > 1) and (el2[1] == 1)):
		Compset.set(E1set.get() + E2set.get() + str(el1[1]))
	elif ((el1[1] > 1) and (el2[1] > 1) and (el1[1]%2 == 0) and (el2[1]%2 == 0)):
		if (((el1[1] == 2) and (el2[1] == 2)) or ((el1[1] == 4) and (el2[1] == 4))):
			Compset.set(E1set.get() + E2set.get())
		elif ((el1[1] == 2) and (el2[1] != 2)):
			Compset.set(E1set.get() + str(math.ceil((el2[1])/2)) + E2set.get())
		elif ((el1[1] != 2) and (el2[1] == 2)):
			Compset.set(E1set.get() + E2set.get() + str(math.ceil((el1[1])/2)))
		else:
			Compset.set(E1set.get() + str(math.ceil((el2[1])/2)) + E2set.get() + str(math.ceil((el1[1])/2)))
	elif ((el1[1] > 1) and (el2[1] > 1)):
		Compset.set(E1set.get() + str(el2[1]) + E2set.get() + str(el1[1]))

def show_Data_Labels():
	gen_compound(globals()[E1set.get()], globals()[E2set.get()])
	MWset.set(round(globals()['MOL_WEIGHT'], 4))
	Vset.set(globals()['VALENCE'])
	SWset.set(gen_mEq_per_L(Tset.get(), SVset.get(), MWset.get(), Vset.get()))
	clear_Data_Labels()
	Countset.set(int(gen_count(int(Endset.get()) + int(Multset.get()), int(Startset.get())) / int(Multset.get())))
	count = int(Countset.get())
	
	for i in range (count):
		
		result = gen_target(float(Startset.get()), i*float(Multset.get()))
		
		T_val_label_text = tk.StringVar()
		T_val_label_text.set(result)
		T_val_label = tk.Label(root, textvariable=T_val_label_text, width=10)
		T_val_label.grid(row=1+i, column=4)

		SV_val_label_text = tk.StringVar()
		SV_val_label_text.set(SVset.get())
		SV_val_label = tk.Label(root, textvariable=SV_val_label_text, width=10)
		SV_val_label.grid(row=1+i, column=5)

		W_val_label_text = tk.StringVar()
		W_val_label_text.set((gen_mEq_per_L(result, SVset.get(), MWset.get(), Vset.get())))
		W_val_label = tk.Label(root, textvariable=W_val_label_text, width=10)
		W_val_label.grid(row=1+i, column=6)	
	
	MW_val_label_text.set(MWset.get())	
	El1_in_label_text.set(E1set.get())	
	El2_in_label_text.set(E2set.get())
	E1_val_label_text.set(globals()[E1set.get()])
	E2_val_label_text.set(globals()[E2set.get()])
	# ~ E1_val_label_text.set(globals()[E1set.get()][0])
	# ~ E2_val_label_text.set(globals()[E2set.get()][0])

def clear_Data_Labels():
	count = int(Countset.get())
	for i in range (count):
		
		T_val_label_text = tk.StringVar()
		T_val_label_text.set("")
		T_val_label = tk.Label(root, textvariable=T_val_label_text, width=10)
		T_val_label.grid(row=1+i, column=4)

		SV_val_label_text = tk.StringVar()
		SV_val_label_text.set("")
		SV_val_label = tk.Label(root, textvariable=SV_val_label_text, width=10)
		SV_val_label.grid(row=1+i, column=5)

		W_val_label_text = tk.StringVar()
		W_val_label_text.set("")
		W_val_label = tk.Label(root, textvariable=W_val_label_text, width=10)
		W_val_label.grid(row=1+i, column=6)


####################################################
################ Entry Declarations ################

Tset = 		tk.StringVar()
SVset = 	tk.StringVar()
Vset = 		tk.StringVar()
TVset = 	tk.StringVar()
MWset = 	tk.StringVar()
SWset = 	tk.StringVar()
E1set = 	tk.StringVar()
E2set = 	tk.StringVar()
Compset = 	tk.StringVar()

Startset = 	tk.StringVar()
Endset = 	tk.StringVar()
Multset = 	tk.StringVar()
Countset = 	tk.StringVar()

Tset_entry = 	tk.Entry(root, textvariable=Tset, width=14)
SVset_entry = 	tk.Entry(root, textvariable=SVset,  width=14)
Vset_entry = 	tk.Entry(root, textvariable=Vset, width=14)
TVset_entry = 	tk.Entry(root, textvariable=TVset, width=14)
MWset_entry = 	tk.Entry(root, textvariable=MWset, width=14)
SWset_entry = 	tk.Entry(root, textvariable=SWset, width=14)
E1set_entry = 	tk.Entry(root, textvariable=E1set, width=14)
E2set_entry = 	tk.Entry(root, textvariable=E2set, width=14)
Compset_entry = tk.Entry(root, textvariable=Compset, width=14)

Startset_entry 	= tk.Entry(root, textvariable=Startset, width=14)
Endset_entry 	= tk.Entry(root, textvariable=Endset, width=14)
Multset_entry 	= tk.Entry(root, textvariable=Multset, width=14)
Countset_entry 	= tk.Entry(root, textvariable=Countset, width=14)

Tset.set(100)
SVset.set(0.25)
Vset.set(Na[1] + Cl[1])
TVset.set(globals()['TVALENCE'])
MWset.set(Na[0] + Cl[0])
SWset.set(0)
E1set.set("Na")
E2set.set("Cl")
Compset.set("Na"+"Cl")

Startset.set(100)
Endset.set(150)
Multset.set(5)
Countset.set(int(gen_count(int(Endset.get()) + int(Multset.get()), int(Startset.get())) / int(Multset.get())))

Tset_entry.grid		(row=0,  column=1)
SVset_entry.grid	(row=1,  column=1)
Vset_entry.grid		(row=2,  column=1)
TVset_entry.grid	(row=3,  column=1)
MWset_entry.grid    (row=4,  column=1)
SWset_entry.grid 	(row=5,  column=1)
E1set_entry.grid 	(row=6,  column=1)
E2set_entry.grid 	(row=7,  column=1)
Compset_entry.grid 	(row=8,  column=1)

Startset_entry.grid (row=10,  column=1)
Endset_entry.grid 	(row=11,  column=1)
Multset_entry.grid 	(row=12, column=1)
Countset_entry.grid (row=13, column=1)

####################################
########## Create Labels ##########

Target_in_label   	= tk.Label(root, text="mEq/L")
SVolume_in_label   	= tk.Label(root, text="SVOL")
Weight_in_label   	= tk.Label(root, text="SOLUTE mg")
MWeight_in_label 	= tk.Label(root, text="MWEIGHT")

El1_in_label = tk.StringVar()
El1_in_label_text = tk.StringVar()
El1_in_label_text.set(E1set.get())
El1_in_label = tk.Label(root, textvariable=El1_in_label_text, width=12)
El1_in_label.grid(row=0, column=8)

El2_in_label = tk.StringVar()
El2_in_label_text = tk.StringVar()
El2_in_label_text.set(E2set.get())
El2_in_label = tk.Label(root, textvariable=El2_in_label_text, width=12)
El2_in_label.grid(row=0, column=9)

target_label = tk.StringVar()
target_label_text = tk.StringVar()
target_label_text.set("Target mEq/L")
target_label = tk.Label(root, textvariable=target_label_text, width=12)
target_label.grid(row=0, column=2)

svol_label = tk.StringVar()
svol_label_text = tk.StringVar()
svol_label_text.set("Solvent Vol L")
svol_label = tk.Label(root, textvariable=svol_label_text, width=12)
svol_label.grid(row=1, column=2)

val_label = tk.StringVar()
val_label_text = tk.StringVar()
val_label_text.set("Net Valence")
val_label = tk.Label(root, textvariable=val_label_text, width=10)
val_label.grid(row=2, column=2)

tval_label = tk.StringVar()
tval_label_text = tk.StringVar()
tval_label_text.set("Total Valence")
tval_label = tk.Label(root, textvariable=tval_label_text, width=11)
tval_label.grid(row=3, column=2)

mweight_label = tk.StringVar()
mweight_label_text = tk.StringVar()
mweight_label_text.set("Mol Weight")
mweight_label = tk.Label(root, textvariable=mweight_label_text, width=10)
mweight_label.grid(row=4, column=2)

swt_label = tk.StringVar()
swt_label_text = tk.StringVar()
swt_label_text.set("Solute Weight mg")
swt_label = tk.Label(root, textvariable=swt_label_text, width=14)
swt_label.grid(row=5, column=2)

el1_label = tk.StringVar()
el1_label_text = tk.StringVar()
el1_label_text.set("Element 1")
el1_label = tk.Label(root, textvariable=el1_label_text, width=14)
el1_label.grid(row=6, column=2)

el2_label = tk.StringVar()
el2_label_text = tk.StringVar()
el2_label_text.set("Element 2")
el2_label = tk.Label(root, textvariable=el2_label_text, width=14)
el2_label.grid(row=7, column=2)

comp_label = tk.StringVar()
comp_label_text = tk.StringVar()
comp_label_text.set("Compound")
comp_label = tk.Label(root, textvariable=comp_label_text, width=14)
comp_label.grid(row=8, column=2)

start_label = tk.StringVar()
start_label_text = tk.StringVar()
start_label_text.set("Start Target")
start_label = tk.Label(root, textvariable=start_label_text, width=14)
start_label.grid(row=10, column=2)

end_label = tk.StringVar()
end_label_text = tk.StringVar()
end_label_text.set("End Target")
end_label = tk.Label(root, textvariable=end_label_text, width=10)
end_label.grid(row=11, column=2)

mult_label = tk.StringVar()
mult_label_text = tk.StringVar()
mult_label_text.set("Loop Mult")
mult_label = tk.Label(root, textvariable=mult_label_text, width=10)
mult_label.grid(row=12, column=2)

count_label = tk.StringVar()
count_label_text = tk.StringVar()
count_label_text.set("Loop Count")
count_label = tk.Label(root, textvariable=count_label_text, width=10)
count_label.grid(row=13, column=2)

###########

T_val		= tk.StringVar()
SV_val		= tk.StringVar()
W_val		= tk.StringVar()
MW_val 		= tk.StringVar()
E1_val		= tk.StringVar()
E2_val		= tk.StringVar()

T_val_label_text = tk.StringVar()
T_val_label_text.set("100")
T_val_label = tk.Label(root, textvariable=T_val_label_text, width=10)
T_val_label.grid(row=1, column=4)

SV_val_label_text = tk.StringVar()
SV_val_label_text.set("0.25")
SV_val_label = tk.Label(root, textvariable=SV_val_label_text, width=10)
SV_val_label.grid(row=1, column=5)

W_val_label_text = tk.StringVar()
W_val_label_text.set(gen_mEq_per_L(Tset.get(), SVset.get(), MWset.get(), Vset.get()))
W_val_label = tk.Label(root, textvariable=W_val_label_text, width=10)
W_val_label.grid(row=1, column=6)

MW_val_label_text = tk.StringVar()
MW_val_label_text.set(Na[0] + Cl[0])
MW_val_label = tk.Label(root, textvariable=MW_val_label_text, width=10)
MW_val_label.grid(row=1, column=7)

E1_val_label_text = tk.StringVar()
E1_val_label_text.set(Na[0])
E1_val_label = tk.Label(root, textvariable=E1_val_label_text, width=10)
E1_val_label.grid(row=1, column=8)

E2_val_label_text = tk.StringVar()
E2_val_label_text.set(Cl[0])
E2_val_label = tk.Label(root, textvariable=E2_val_label_text, width=10)
E2_val_label.grid(row=1, column=9)

#####################################################
################ The Label Generator ################
for a in range(30):
	root.grid_columnconfigure(a,  minsize=column_size)
	root.grid_rowconfigure(a,  minsize=row_size)
	Target_in_label.grid(   row=0, column=4)
	SVolume_in_label.grid(  row=0, column=5)
	Weight_in_label.grid(   row=0, column=6)
	MWeight_in_label.grid( 	row=0, column=7)
	El1_in_label.grid( 		row=0, column=8)
	El2_in_label.grid( 		row=0, column=9)
 
root.update()
root.mainloop()


# ~ MILLI 	= 1.0e-3
# ~ MICRO 	= 1.0e-6
# ~ NANO 	= 1.0e-9
# ~ PICO 	= 1.0e-12
# ~ KILO 	= 1.0e3
# ~ MEGA 	= 1.0e6
# ~ GIGA 	= 1.0e9
# ~ TERA 	= 1.0e12 

# ~ ## Molecular Weights of Elements
# ~ HYDROGEN	= 1.008
# ~ HELIUM 		= 4.026
# ~ LITHIUM		= 6.94
# ~ BERYLLIUM 	= 9.012
# ~ BORON		= 10.81
# ~ CARBON		= 12.011
# ~ NITROGEN	= 14.077
# ~ OXYGEN		= 15.999
# ~ FLUORINE	= 18.998
# ~ NEON		= 20.180
# ~ SODIUM		= 22.99
# ~ MAGNESIUM 	= 24.305
# ~ ALUMINUM	= 26.982
# ~ SILICON		= 28.085
# ~ PHOSPHORUS 	= 30.974
# ~ SULFUR		= 32.06
# ~ CHLORINE	= 35.45
# ~ ARGON		= 39.948
# ~ POTASSIUM	= 39.098
# ~ CALCIUM		= 40.078

# ~ ## Valences of Elements
# ~ HYDROGEN_V		= 1
# ~ HELIUM_V 		= 2
# ~ LITHIUM_V		= 1
# ~ BERYLLIUM_V 	= 2
# ~ BORON_V			= 3
# ~ CARBON_V		= 4
# ~ NITROGEN_V		= 3
# ~ OXYGEN_V		= 2
# ~ FLUORINE_V		= 1
# ~ NEON_V			= 8
# ~ SODIUM_V		= 1
# ~ MAGNESIUM_V 	= 2
# ~ ALUMINUM_V		= 3
# ~ SILICON_V		= 4
# ~ PHOSPHORUS_V 	= 3
# ~ SULFUR_V		= 2
# ~ CHLORINE_V		= 1
# ~ ARGON_V			= 8
# ~ POTASSIUM_V		= 1
# ~ CALCIUM_V		= 2


# ~ def gen_element_data ():
	# ~ globals()['MOL_WEIGHT'] = 0
	# ~ globals()['VALENCE'] = 0
	# ~ if (E1set.get() == "H"):
		# ~ globals()['MOL_WEIGHT'] += H[0]
		# ~ globals()['VALENCE'] += H[1]
	# ~ elif (E1set.get() == "He"):
		# ~ globals()['MOL_WEIGHT'] += He[0]
		# ~ globals()['VALENCE'] += He[1]
	# ~ elif (E1set.get() == "Li"):
		# ~ globals()['MOL_WEIGHT'] += Li[0]
		# ~ globals()['VALENCE'] += Li[1]
	# ~ elif (E1set.get() == "Be"):
		# ~ globals()['MOL_WEIGHT'] += Be[0]
		# ~ globals()['VALENCE'] += Be[1]
	# ~ elif (E1set.get() == "B"):
		# ~ globals()['MOL_WEIGHT'] += B[0]
		# ~ globals()['VALENCE'] += B[1]
	# ~ elif (E1set.get() == "C"):
		# ~ globals()['MOL_WEIGHT'] += C[0]
		# ~ globals()['VALENCE'] += C[1]
	# ~ elif (E1set.get() == "N"):
		# ~ globals()['MOL_WEIGHT'] += N[0]
		# ~ globals()['VALENCE'] += N[1]
	# ~ elif (E1set.get() == "O"):
		# ~ globals()['MOL_WEIGHT'] += O[0]
		# ~ globals()['VALENCE'] += O[1]
	# ~ elif (E1set.get() == "F"):
		# ~ globals()['MOL_WEIGHT'] += F[0]
		# ~ globals()['VALENCE'] += F[1]
	# ~ elif (E1set.get() == "Ne"):
		# ~ globals()['MOL_WEIGHT'] += Ne[0]
		# ~ globals()['VALENCE'] += Ne[1]
	# ~ elif (E1set.get() == "Na"):
		# ~ globals()['MOL_WEIGHT'] += Na[0]
		# ~ globals()['VALENCE'] += Na[1]
	# ~ elif (E1set.get() == "Mg"):
		# ~ globals()['MOL_WEIGHT'] += Mg[0]
		# ~ globals()['VALENCE'] += Mg[1]
	# ~ elif (E1set.get() == "Al"):
		# ~ globals()['MOL_WEIGHT'] += Al[0]
		# ~ globals()['VALENCE'] += Al[1]
	# ~ elif (E1set.get() == "Si"):
		# ~ globals()['MOL_WEIGHT'] += Si[0]
		# ~ globals()['VALENCE'] += Si[1]
	# ~ elif (E1set.get() == "P"):
		# ~ globals()['MOL_WEIGHT'] += P[0]
		# ~ globals()['VALENCE'] += P[1]
	# ~ elif (E1set.get() == "S"):
		# ~ globals()['MOL_WEIGHT'] += S[0]
		# ~ globals()['VALENCE'] += S[1]
	# ~ elif (E1set.get() == "Cl"):
		# ~ globals()['MOL_WEIGHT'] += Cl[0]
		# ~ globals()['VALENCE'] += Cl[1]
	# ~ elif (E1set.get() == "Ar"):
		# ~ globals()['MOL_WEIGHT'] += Ar[0]
		# ~ globals()['VALENCE'] += Ar[1]
	# ~ elif (E1set.get() == "K"):
		# ~ globals()['MOL_WEIGHT'] += K[0]
		# ~ globals()['VALENCE'] += K[1]
	# ~ elif (E1set.get() == "Ca"):
		# ~ globals()['MOL_WEIGHT'] += Ca[0]
		# ~ globals()['VALENCE'] += Ca[1]
	# ~ else:
		# ~ return -1
	
	# ~ if (E2set.get() == "H"):
		# ~ globals()['MOL_WEIGHT'] += H[0]
		# ~ globals()['VALENCE'] += H[1]
	# ~ elif (E2set.get() == "He"):
		# ~ globals()['MOL_WEIGHT'] += He[0]
		# ~ globals()['VALENCE'] += He[1]
	# ~ elif (E2set.get() == "Li"):
		# ~ globals()['MOL_WEIGHT'] += Li[0]
		# ~ globals()['VALENCE'] += Li[1]
	# ~ elif (E2set.get() == "Be"):
		# ~ globals()['MOL_WEIGHT'] += Be[0]
		# ~ globals()['VALENCE'] += Be[1]
	# ~ elif (E2set.get() == "B"):
		# ~ globals()['MOL_WEIGHT'] += B[0]
		# ~ globals()['VALENCE'] += B[1]
	# ~ elif (E2set.get() == "C"):
		# ~ globals()['MOL_WEIGHT'] += C[0]
		# ~ globals()['VALENCE'] += C[1]
	# ~ elif (E2set.get() == "N"):
		# ~ globals()['MOL_WEIGHT'] += N[0]
		# ~ globals()['VALENCE'] += N[1]
	# ~ elif (E2set.get() == "O"):
		# ~ globals()['MOL_WEIGHT'] += O[0]
		# ~ globals()['VALENCE'] += O[1]
	# ~ elif (E2set.get() == "F"):
		# ~ globals()['MOL_WEIGHT'] += F[0]
		# ~ globals()['VALENCE'] += F[1]
	# ~ elif (E2set.get() == "Ne"):
		# ~ globals()['MOL_WEIGHT'] += Ne[0]
		# ~ globals()['VALENCE'] += Ne[1]
	# ~ elif (E2set.get() == "Na"):
		# ~ globals()['MOL_WEIGHT'] += Na[0]
		# ~ globals()['VALENCE'] += Na[1]
	# ~ elif (E2set.get() == "Mg"):
		# ~ globals()['MOL_WEIGHT'] += Mg[0]
		# ~ globals()['VALENCE'] += Mg[1]
	# ~ elif (E2set.get() == "Al"):
		# ~ globals()['MOL_WEIGHT'] += Al[0]
		# ~ globals()['VALENCE'] += Al[1]
	# ~ elif (E2set.get() == "Si"):
		# ~ globals()['MOL_WEIGHT'] += Si[0]
		# ~ globals()['VALENCE'] += Si[1]
	# ~ elif (E2set.get() == "P"):
		# ~ globals()['MOL_WEIGHT'] += P[0]
		# ~ globals()['VALENCE'] += P[1]
	# ~ elif (E2set.get() == "S"):
		# ~ globals()['MOL_WEIGHT'] += S[0]
		# ~ globals()['VALENCE'] += S[1]
	# ~ elif (E2set.get() == "Cl"):
		# ~ globals()['MOL_WEIGHT'] += Cl[0]
		# ~ globals()['VALENCE'] += Cl[1]
	# ~ elif (E2set.get() == "Ar"):
		# ~ globals()['MOL_WEIGHT'] += Ar[0]
		# ~ globals()['VALENCE'] += Ar[1]
	# ~ elif (E2set.get() == "K"):
		# ~ globals()['MOL_WEIGHT'] += K[0]
		# ~ globals()['VALENCE'] += K[1]
	# ~ elif (E2set.get() == "Ca"):
		# ~ globals()['MOL_WEIGHT'] += Ca[0]
		# ~ globals()['VALENCE'] += Ca[1]
	# ~ else:
		# ~ return -1

	# ~ print("MOL_WEIGHT\t", globals()['MOL_WEIGHT'])
	# ~ print("VALENCE\t", globals()['VALENCE'])
