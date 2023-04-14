import numpy as np
import matplotlib.pyplot as plt
from src.simulation import Simulation

def main():
    
    # Define initial conditions
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

    sim = Simulation(t0, tf, dt, x0, propensities, reactions)   
    sim.run()

    t = sim.t_list
    x = sim.x_list


if __name__ == "__main__":
    main()