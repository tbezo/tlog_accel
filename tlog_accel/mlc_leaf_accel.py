"""Class to calculate leaf acceleration from Trajectory Log Files."""
import numpy as np
from pylinac import TrajectoryLog
from scipy.signal import find_peaks

class MlcLeafAccel:   
    """Class to calculate leaf acceleration and leaf speeds from pylinac.""" 
        
    DT = 0.02 # Trajectory Log sampling interval 
    
    def __init__(self, tlog_path: str):        
        """Class init function.
        
        Init function that calculates the accelerations for each leaf from 
        the Trajectory log file through methods.

        Parameters
        ----------
        tlog_path : str
            File path to the Trajectory Logfile to process.

        Returns
        -------
        None.

        """        
        self.tlog = TrajectoryLog(tlog_path)
        self.leaf_pos = self.__extract_leaf_data()
        self.leaf_speeds = self.__calc_speed()
        self.leaf_accels =  self.__calc_accel()
        self.accel_peaks = self.__get_peaks()
        
    def __extract_leaf_data(self) -> list:
        """
        Return a list of the actual position data for each leaf.
        
        Each list entry is a list with leaf positions spaced 20ms apart.

        Returns
        -------
        list
            List of leaf positions over time.

        """
        lpos = [leaf.actual for leaf in self.tlog.axis_data.mlc.leaf_axes.values()]
        return lpos

    def __calc_speed(self) -> list:
        """
        Return a list with the calculated gradients for each leaf.
        
        The gradient is equivalent to the leaf speed.

        Returns
        -------
        list
            List with leaf speeds over time.

        """
        lspeeds = [np.gradient(leaf, self.DT) for leaf in self.leaf_pos]
        return lspeeds
    
    def __calc_accel(self) -> list:
        """
        Calculate leaf acceleration for each leaf.

        Returns
        -------
        list
            List of leaf accelerations over time.

        """
        laccels = [np.gradient(leaf, self.DT) for leaf in self.leaf_speeds]
        return laccels
       
    def __get_peaks(self, min_accel: float = 10.) -> list:
        """
        Find positive and negative acceleration peaks.
        
        Returned values are sorted by time.

        Parameters
        ----------
        min_accel : float, optional
            Parameter for scipy.signal.find_peaks() height parameter. 
            The default is 10.

        Returns
        -------
        list
            Returns a list of tupels containing the x-axis position and the
            acceleration value.

        """
        accel_peaks = []
        for accels in self.leaf_accels:
            pos_peaks = find_peaks(accels, height=min_accel) # ignore accels < 10
            # get tuple for peak index and acceleration value.
            pos_peaks = list(zip(pos_peaks[0], pos_peaks[1]['peak_heights']))
            neg_peaks = find_peaks(-accels, height=min_accel)
            neg_peaks = list(zip(neg_peaks[0], -neg_peaks[1]['peak_heights']))
            peaks_combined = sorted(pos_peaks + neg_peaks, key=lambda x: x[0])
            accel_peaks.append(peaks_combined)
        return accel_peaks


    def speed_mean(self) -> list:
        """
        Calculate the mean speed for each leaf.

        Returns
        -------
        list
            List with mean travel speed vor each leaf.

        """
        # get indices from maximum acceleration
        accel_peaks_pos = [[pos[0] for pos in peak] 
                           for peak in self.accel_peaks]
        
        # get mean speed values between acceleration phases
        mean_speeds = []
        for leaf, speed in enumerate(self.leaf_speeds):
            """ width of each acceleration peak is roughly 6 indices = 0.12s,
                so we start three values after the peak and end 3 before.
            """
            x = [speed[start+3:stop-3].mean() 
                 for start, stop in 
                 zip(accel_peaks_pos[leaf][::2], 
                     accel_peaks_pos[leaf][1::2])]
            mean_speeds.append(x)
            
        mean_leaf_speed = [np.mean(np.abs(m)) for m in mean_speeds]
        
        return mean_leaf_speed
    
    def speed_mean_std(self) -> list:
        """
        Calculate the standard deviation for the mean leaf speeds.

        Returns
        -------
        list
            List of standard deviations for the mean of each leaf.

        """
        # get indices from maximum acceleration
        accel_peaks_pos = [[pos[0] for pos in peak] 
                           for peak in self.accel_peaks]
        
        mean_speeds_std = []
        for leaf, speed in enumerate(self.leaf_speeds):
            y = [speed[start+2:stop-2].std() 
                 for start, stop in zip(accel_peaks_pos[leaf][::2], 
                                        accel_peaks_pos[leaf][1::2])]
            mean_speeds_std.append(y)
            
        stddev = [np.sqrt(np.sum(np.square(y))) / len(z) for z in mean_speeds_std]
        return stddev

    def accel_mean(self) -> list:
        """
        Calculate the mean of all accelerations for each leaf.
        
        Only interesting when the plan has one repeated fixed velocity.

        Returns
        -------
        list
            List with the mean accelerations for each leaf.

        """
        amean = [np.mean(np.abs([mean[1] for mean in peak])) 
                 for peak in self.accel_peaks]
        return amean
    
    def accel_stats(self, skip_leafs: set[int] = {0,59,60,119}) -> dict:
        """
        Calculate some statistics over all leafs accelerations.
        
        Values for the sacrificial leafs are ignored.

        Parameters
        ----------
        skip_leafs : set[int], optional
            Leaf indices of all sacrificial Leafs to exclude. The default is 
            {0,59,60,119}.

        Returns
        -------
        dict
            Dict contianing the total mean, min, max and 
            standard deviation for leaf accelerations.

        """
        accel_filtered = [x for i, x in enumerate(self.accel_mean()) 
                          if i not in skip_leafs]
        results_dict = {
            'accel_total_mean': np.mean(accel_filtered),
            'accel_max': np.max(accel_filtered),
            #'accel_max_leaf': ,
            'accel_min': np.min(accel_filtered),
            #'accel_min_leaf': ,
            'accel_std': np.std(accel_filtered)
            }
        return results_dict
