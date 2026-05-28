# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:55:55 2026

@author: bez0t
"""
import matplotlib.pyplot as plt
from MlcLeafAccel import MlcLeafAccel

myaccel = MlcLeafAccel(r'c:\temp\MLC_accel25.bin')

print(f"Daten für Leaf 62:\nBeschleunigung: {myaccel.accel_mean()[60]}" 
      f"\nGeschwindigkeit: {myaccel.speed_mean()[60]} "
      f"\nStandardabweichung: {myaccel.speed_mean_std()[60]}")

plt.plot(myaccel.leaf_accels[61])