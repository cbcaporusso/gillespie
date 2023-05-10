import numpy as np
import matplotlib.pyplot as plt
from src.simulation import Simulation, SpinFlip
from src.traj import Trajectories

def main():
    
    # Define initial conditions
    nruns = 100

    t0 = 0
    tf = 100_000
    dt = 0.1

    gammas = np.linspace(0.8, 1.0, 3)
    r = 0.1

    N = 20
    N1 = 1

    x0 = np.zeros(N)
    # randomly initialize 100 spins to 1
    x0[np.random.randint(0, N, size=N1)] = 1

    for gamma in gammas:
        run_simulation_almostallspin0(nruns, t0, tf, dt, x0, gamma, r,)


def run_simulation_almostallspin0(nruns, t0, tf, dt, x0, gamma, r):
    
    print(f"gamma = {gamma}")
    print(f"r = {r}")
    
    trjs = Trajectories(t0, tf)
    for run in range(nruns):
        print("Run {}".format(run), end="\r")
        sim = SpinFlip(t0, tf, dt, gamma, r, x0)
        t, m = sim.run()
        plt.plot(t, m)
        trjs.add(t, m)

    t_avg, m_avg = trjs.average(50)
    trjs.save(sim)

    print('')
    #plt.plot(t_avg, m_avg, label="Average", color="black", linewidth=3)
    #plt.show()

if __name__ == "__main__":
    main()