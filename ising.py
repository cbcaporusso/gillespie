import numpy as np
import matplotlib.pyplot as plt
from src.simulation import Simulation, SpinFlip

def main():
    
    # Define initial conditions
    nruns = 100

    t0 = 0
    tf = 10_000
    dt = 0.001

    gamma = 2.0
    r = 0.5

    N = 500

    x0 = np.ones(N)
    for run in range(nruns):
        sim = SpinFlip(t0, tf, dt, gamma, r, x0)
        t, m = sim.run()
        plt.plot(t, m, label="Run {}".format(run))

    plt.show()

if __name__ == "__main__":
    main()