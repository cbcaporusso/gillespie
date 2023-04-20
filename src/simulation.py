import numpy as np

class Simulation():
    """
    A class to simulate a stochastic system using Gillespie algorithm.
    """

    def __init__(self, t0: float, tf: float, dt: float,
                 x0, propensities, reactions):
        """
        Initialize the simulation.

        Parameters
        ----------
        t0 : float
            Initial time.
        tf : float
            Final time.
        dt : float
            Time step.
        x0 : list of int
            Initial state.
        propensities : list of functions
            List of propensities functions.
        reactions : list of functions
            List of reaction functions.
        """
        self.t0 = t0
        self.tf = tf
        self.dt = dt
        self.x0 = x0
        self.propensities = propensities
        self.reactions = reactions
        self.t = t0
        self.x = x0
        self.t_list = [t0]
        self.x_list = [x0]

    def run(self):
        """
        Run the simulation.
        """
        while self.t < self.tf:
            self.step()

    def step(self):
        """
        Perform a single step of the simulation.
        """
        # Compute propensities
        a = [p(self.t, self.x) for p in self.propensities]
        # Compute total propensity
        a0 = sum(a)
        # Compute time to next reaction
        tau = np.random.exponential(scale=1/a0)
        # Compute next reaction
        r = np.random.choice(range(len(a)), p=[a_i/a0 for a_i in a])
        # Update time
        self.t += tau
        # Update state
        self.x = self.reactions[r](self.t, self.x)
        # Store time and state
        self.t_list.append(self.t)
        self.x_list.append(self.x)

    def get_time(self):
        """
        Return time points.
        """
        return self.t_list

    def get_state(self):
        """
        Return state points.
        """
        return self.x_list


class SpinFlip():

    def __init__(self, t0, tf, dt, gamma, r, x0) -> None:
        
        self.t0 = t0
        self.tf = tf
        self.dt = dt

        self.gamma = gamma
        self.r = r 

        self.t = t0       
        self.spins = np.copy(x0)

    def run(self):
        """
        Run the simulation.
        """
        t_arr = []
        m_arr = []
        while self.t < self.tf:
            self.step()
            t_arr.append(self.t)
            m_arr.append(self.magnetization())

        return t_arr, m_arr

    def step(self):
        """
        Perform a single step of the simulation.
        """

        if np.all(self.spins == 0):
            self.t = self.tf
            return None

        # choose a spin to flip
        i = np.random.randint(0, len(self.spins))
        # Compute the spin flip probability
        a0 = self.trans_prob(i)
        if a0 > 0:
            # Compute time to next reaction
            tau = np.random.exponential(scale=1/a0)
            # Choose if the spin will flip 
            prob = np.random.choice(range(2), p=[1-a0, a0])
            # Update time
            self.t += tau
            # Update state
            if prob == 1:
                self._switch(i)

    def _switch(self, i):
        spin = self.spins[i]
        if spin == 0:
            self.spins[i] += 1
        elif spin == 1:
            self.spins[i] -= 1 

    def trans_prob(self, i):
        x = self.spins
        spin = self.spins[i]

        w10 = self.r
        
        xp1 = x[i+1] if i < len(x)-1 else x[0]
        xm1 = x[i-1] if i > 0 else x[-1]

        n = xp1 + xm1
        #w01 = 1.0
        w01 = self.gamma * n / 2.0
        
        #norm = w10 + w01

        if spin == 1:
            return w10 #/ norm
        elif spin == 0:
            return w01 #/ norm
        
    def magnetization(self):
        return np.mean(self.spins)