import numpy as np
import itertools as itertools

class Trajectories():
    """
    Class grouping different the trajectories of a simulation for averaging
    """

    def __init__(self, t0, tf):
        """
        Parameters
        ----------
        trj : list of arrays
            List of arrays with the trajectories
        """
        self.times = []
        self.trjs = []
        self.counter = 0

        self.t0 = t0
        self.tf = tf

    @staticmethod
    def init_from_trjs(times, trj):
        """
        Initialize the class from a list of trajectories

        Parameters
        ----------
        trj : list of arrays
            List of arrays with the trajectories
        """
        trjs = Trajectories()
        
        for i in range(len(times)):
            trjs.times.append(times[i])
            trjs.trjs.append(trj[i])
            trjs.counter += 1

        return trjs

    def add(self, t, trj):
        """
        Add a new trajectory to the list

        Parameters
        ----------
        trj : array
            Array with the trajectory
        """
        self.times.append(t)
        self.trjs.append(trj)
        self.counter += 1
        
    def average(self, dt):
        """
        Compute the average of the trajectories making a binning over times
        """

        #t_flatten = itertools.chain.from_iterable(self.times)
        tmin = self.t0
        #t_flatten = itertools.chain.from_iterable(self.times)
        tmax = self.tf 
        #max(list(t_flatten))
        t = np.arange(tmin, tmax, dt)
        m = np.zeros(len(t))
        m_count = np.zeros(len(t))
        for i in range(len(t)):
            for j in range(self.counter):
                t_index = np.argmin(np.abs(t[i] - self.times[j]))
                m[i] += self.trjs[j][t_index]
                m_count[i] += 1
        m = np.where(m_count > 0, m/m_count, 0)
        return t, m