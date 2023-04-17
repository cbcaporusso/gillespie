import numpy as np
import matplotlib.pyplot as plt
from src.simulation import Simulation

def main():
    
    # Define initial conditions
    nruns = 25

    t0 = 0
    tf = 10
    dt = 0.1

    N = 500
    beta = 2
    gamma = 0.5

    I0 = 3
    x0 = [N - I0, I0, 0]

    propensities = [ lambda t, x: beta * x[0] * x[1] / N,
                     lambda t, x: gamma * x[1] ]
    
    reactions = [lambda t, x: [x[0] - 1, x[1] + 1, x[2]],
                 lambda t, x: [x[0], x[1] - 1, x[2] + 1] ]

    for i in range(nruns):

        sim = Simulation(t0, tf, dt, x0, propensities, reactions)   
        sim.run()

        t = sim.t_list
        s_array = [ x[0] for x in sim.x_list]
        i_array = [ x[1] for x in sim.x_list]
        r_array = [ x[2] for x in sim.x_list]
    
        plt.plot(t, s_array, label="S")
        plt.plot(t, i_array, label="I")
        plt.plot(t, r_array, label="R")
    
    
    plt.show()


if __name__ == "__main__":
    main()