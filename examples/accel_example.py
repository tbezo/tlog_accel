# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:55:55 2026

@author: bez0t
"""
import matplotlib.pyplot as plt
from tlog_accel import MlcLeafAccel

myaccel = MlcLeafAccel(r'c:\temp\MLC_accel25.bin')

print(f"Data for Leaf 62:\nAcceleration: {myaccel.accel_mean()[61]}" 
      f"\nVelocity: {myaccel.speed_mean()[61]} "
      f"\nStandard deviation: {myaccel.speed_mean_std()[61]}")

plt.plot(myaccel.leaf_accels[61])
