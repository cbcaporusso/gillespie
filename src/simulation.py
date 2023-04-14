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
