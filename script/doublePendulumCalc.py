#!/usr/bin/env python

"""
Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: April 28, 2024
File Name: doublePendulumCalc.py

This script simulates a double pendulum system and saves the results to CSV files.
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

def double_pendulum(t, y, m1, m2, L1, L2, g):
    """Differential equations for the double pendulum system."""
    a = (m1 + m2) * L1
    b = m2 * L2 * np.cos(y[0] - y[2])
    c = m2 * L1 * np.cos(y[0] - y[2])
    d = m2 * L2

    e = -m2 * L2 * y[3] * y[3] * np.sin(y[0] - y[2]) - g * (m1 + m2) * np.sin(y[0])
    f = m2 * L1 * y[1] * y[1] * np.sin(y[0] - y[2]) - m2 * g * np.sin(y[2])

    return [
        y[1],
        (e * d - b * f) / (a * d - c * b),
        y[3],
        (a * f - c * e) / (a * d - c * b)
    ]

def simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions, filename):
    """Simulates the double pendulum system and saves results to a CSV file."""
    time_span = (0, 10)
    num_points = 10000

    sol = solve_ivp(
        lambda t, y: double_pendulum(t, y, m1, m2, L1, L2, g),
        time_span,
        initial_conditions,
        method='RK45',
        t_eval=np.linspace(time_span[0], time_span[1], num_points)
    )

    columns = ['t', 'x1', 'y1', 'x2', 'y2', 'theta1', 'theta2', 'omega1', 'omega2']
    data = {
        't': sol.t,
        'x1': L1 * np.sin(sol.y[0]),
        'y1': -L1 * np.cos(sol.y[0]),
        'x2': L1 * np.sin(sol.y[0]) + L2 * np.sin(sol.y[2]),
        'y2': -L1 * np.cos(sol.y[0]) - L2 * np.cos(sol.y[2]),
        'theta1': sol.y[0],
        'theta2': sol.y[2],
        'omega1': sol.y[1],
        'omega2': sol.y[3]
    }

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False)

def run_double_pendulum_simulations():
    """Runs both original and modified simulations of the double pendulum."""
    m1 = 2
    m2 = 1
    L1 = 2
    L2 = 1
    g = 9.8

    initial_conditions_original = [np.pi, 0.0, 1.57, 0.0]
    initial_conditions_modified = [np.pi, 0.001, 1.57, 0.001]

    simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions_original, '../data/python_double_pendulum_original.csv')
    simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions_modified, '../data/python_double_pendulum_modified.csv')

if __name__ == "__main__":
    run_double_pendulum_simulations()

