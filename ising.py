import numpy as np
import matplotlib.pyplot as plt
from src.simulation import Simulation, SpinFlip
from src.traj import Trajectories

def main():
    
    # Define initial conditions
    nruns = 50

    t0 = 0
    tf = 1000
    dt = 0.1

    gamma = 0.2
    r = 0.1

    N = 10_000

    # random inizitalize array to 0 or 1
    #x0 = np.random.randint(2, size=N)
    x0 = np.zeros(N)
    x0[10] = 1

    trjs = Trajectories(t0, tf)
    for run in range(nruns):
        print("Run {}".format(run))
        sim = SpinFlip(t0, tf, dt, gamma, r, x0)
        t, m = sim.run()
        plt.plot(t, m)
        trjs.add(t, m)

    t_avg, m_avg = trjs.average(10)
    plt.plot(t_avg, m_avg, label="Average", color="black", linewidth=3)

    plt.show()

if __name__ == "__main__":
    main()