import numpy as np
import itertools as itertools
import os, sys

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

        self.avg = False
        
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

        self.t_avg = t
        self.m_avg = m

        self.avg = True

        return t, m
    
    def save(self, sim, path="data"):
        """
        Save the trajectories in a specific path
        """

        gamma = sim.gamma
        r = sim.r

        x0 = sim.spins

        n_spins = len(x0)
        m0 = np.mean(x0)

        sim_path = f'trjs/n_{n_spins}_m0_{m0:.2f}_gamma_{gamma:.2f}_r_{r:.2f}/'

        os.makedirs(sim_path, exist_ok=True)
        os.makedirs('trjs/avgs', exist_ok=True)

        # Save the trajectories
        for i in range(self.counter):
            np.savetxt(sim_path + f'traj_{i}.dat', np.column_stack((self.times[i], self.trjs[i])))

        # Save the average
        if self.avg:
            np.savetxt(f'trjs/avgs/avg_n_{n_spins}_m0_{m0:.2f}_gamma_{gamma:.2f}_r_{r:.2f}.dat', np.column_stack((self.t_avg, self.m_avg)))
        else:
            print("Average not computed")
            self.average(10)
            np.savetxt(f'trjs/avgs/avg_n_{n_spins}_m0_{m0:.2f}_gamma_{gamma:.2f}_r_{r:.2f}.dat', np.column_stack((self.t_avg, self.m_avg)))
