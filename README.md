# Calculating Leaf Acceleration from Trajetory Logfiles
With tlog_accel you can calculate leaf accelerations from Varian Trajetory Logfiles. The module uses the incredible [pylinac](https://github.com/jrkerns/pylinac) library to read the position data and calculates the acceleration by gradient formation.

## Creating an Irradiation Plan
For plan creation please follow the [pylinac documentation](https://pylinac.readthedocs.io/en/latest/plan_generator.html) and generate a [MLC speed plan](https://pylinac.readthedocs.io/en/latest/plan_generator.html#mlc-speed) with four or five subfield that utilize the maximum travel speed. There is code in the example folder for this project.

## Analyzing the Trajectory Logfiles
After you finished irradiating the plan copy the Trajectory Logfile to a place were you can do the analysis. There is a small example in the example folder for the project. A minimal code could look like this:
```python
from tlog_accel import MlcLeafAccel

myaccel = MlcLeafAccel(r'c:\temp\MLC_accel25.bin')

print(f"Data for Leaf 61:\nAcceleration: {myaccel.accel_mean()[61]}\n" 
      f"Velocity: {myaccel.speed_mean()[61]\n} "
      f"Standard deviation: {myaccel.speed_mean_std()[61]}")
```
Since pylinac uses sacrificial leaf movements to modulate the leaf speed the first and last leaf of each leaf carriage will not use the speeds you set with pylinac.

