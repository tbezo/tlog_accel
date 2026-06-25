import matplotlib.pyplot as plt
from tlog_accel import MlcLeafAccel

myaccel = MlcLeafAccel(r'c:\temp\MLC_accel25.bin')

# informations for single leaf
print(f"Data for Leaf 61:\nAcceleration: {myaccel.accel_mean()[61]}\n" 
      f"Velocity: {myaccel.speed_mean()[61]}\n"
      f"Standard deviation: {myaccel.speed_mean_std()[61]}")
plt.plot(myaccel.leaf_accels[61])

# statistics
print(myaccel.accel_stats())
