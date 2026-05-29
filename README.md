# Calculating Leaf Acceleration from Trajetory Logfiles
With tlog_accel you can calculate leaf accelerations from Varian Trajectory Logfiles. The module uses the incredible [pylinac](https://github.com/jrkerns/pylinac) library to read the position data and calculates the acceleration by gradient formation.

## Creating an Irradiation Plan
For plan creation please follow the [pylinac documentation](https://pylinac.readthedocs.io/en/latest/plan_generator.html) and generate a [MLC speed plan](https://pylinac.readthedocs.io/en/latest/plan_generator.html#mlc-speed) with four or five subfield that utilize the maximum travel speed. There is code in the example folder for this project.

## Analyzing the Trajectory Logfiles
After you finished irradiating the plan copy the Trajectory Logfile to a place were you can do the analysis. There is a small example in the example folder for the project. A minimal code could look like this:
```python
from tlog_accel import MlcLeafAccel

myaccel = MlcLeafAccel(r'c:\temp\MLC_accel25.bin')

print(f"Data for Leaf 62:\nAcceleration: {myaccel.accel_mean()[61]}\n" 
      f"Velocity: {myaccel.speed_mean()[61]\n} "
      f"Standard deviation: {myaccel.speed_mean_std()[61]}")
	  
print(myaccel.accel_stats())
```
Since pylinac uses sacrificial leaf movements to modulate the leaf speed the first and last leaf of each leaf carriage will not use the speeds you set with pylinac (if you use the example).

## Plotting Leaf Information
With pyplot you can plot the leaf position, velocity and acceleration.
```python
import matplotlib.pyplot as plt

plt.plot(myaccel.leaf_pos[3])
```
<img width="376" height="248" alt="Position" src="https://github.com/user-attachments/assets/bff770e2-5ddc-4f28-8b12-2cd16d29508d" />

```
plt.plot(myaccel.leaf_speeds[3])
```
<img width="377" height="248" alt="Speed" src="https://github.com/user-attachments/assets/3c5ac25a-577c-453f-b533-38f90f3d5956" />

```
plt.plot(myaccel.leaf_accels[3])
```
<img width="382" height="248" alt="Acceleration" src="https://github.com/user-attachments/assets/f355e201-6df0-4c99-a3bd-b3c4520f244d" />


## Install Instructions for pip
```
source ~/venvs/myvenv/bin/activate #optional
pip install git+https://github.com/tbezo/tlog_accel
```
