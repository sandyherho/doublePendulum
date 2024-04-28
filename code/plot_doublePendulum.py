#!/usr/bin/env python

"""
Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: April 28, 2024
File Name: plot_doublePendulum.py

This script plots data from a simulated double pendulum system and saves the plots as images.
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')

class PendulumPlotter:
    def __init__(self, data_file_ori, data_file_mod):
        self.df_ori = pd.read_csv(data_file_ori)
        self.df_mod = pd.read_csv(data_file_mod)

    def plot_single(self, x, y, label_x, label_y, legend_labels, save_path):
        plt.figure()
        plt.plot(x, y, ls='--')
        plt.xlabel(label_x, fontsize=18)
        plt.ylabel(label_y, fontsize=18)
        plt.legend(legend_labels, loc='lower right')
        plt.savefig(save_path, dpi=400)
        plt.close()

    def plot_xy_trajectory(self, x1, y1, x2, y2, legend_labels, save_path):
        plt.figure()
        plt.plot(x1, y1)
        plt.plot(x2, y2)
        plt.xlabel(r'$x$ [m]', fontsize=18)
        plt.ylabel(r'$y$ [m]', fontsize=18)
        plt.legend(legend_labels, loc='lower right')
        plt.savefig(save_path, dpi=400)
        plt.close()

    def plot_phase_space(self, theta1, omega1, theta2, omega2, legend_labels, save_path):
        plt.figure()
        plt.plot(theta1, omega1)
        plt.plot(theta2, omega2)
        plt.xlabel(r'$\theta$ [rad]', fontsize=18)
        plt.ylabel(r'$\dot{\theta}$ [rad/s]', fontsize=18)
        plt.legend(legend_labels)
        plt.savefig(save_path, dpi=400)
        plt.close()

if __name__ == "__main__":
    data_file_ori = '../data/python_double_pendulum_original.csv'
    data_file_mod = '../data/python_double_pendulum_modified.csv'

    plotter = PendulumPlotter(data_file_ori, data_file_mod)

    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['x1'], r'$t$ [s]', r'$x_1$ [m]',
                        ['Original', 'Perturbed'], '../figs/fig2a.png')
    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['y1'], r'$t$ [s]', r'$y_1$ [m]',
                        ['Original', 'Perturbed'], '../figs/fig2b.png')
    
    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['x2'], r'$t$ [s]', r'$x_2$ [m]',
                        ['Original', 'Perturbed'], '../figs/fig2c.png')
    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['y2'], r'$t$ [s]', r'$y_2$ [m]',
                        ['Original', 'Perturbed'], '../figs/fig2d.png')

    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['theta1'], r'$t$ [s]', r'$\theta_1$ [rad]',
                        ['Original', 'Perturbed'], '../figs/fig3a.png')
    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['theta2'], r'$t$ [s]', r'$\theta_2$ [rad]',
                        ['Original', 'Perturbed'], '../figs/fig3b.png')

    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['omega1'], r'$t$ [s]', r'$\dot{\theta}_1$ [rad/s]',
                        ['Original', 'Perturbed'], '../figs/fig3c.png')
    plotter.plot_single(plotter.df_ori['t'], plotter.df_ori['omega2'], r'$t$ [s]', r'$\dot{\theta}_2$ [rad/s]',
                        ['Original', 'Perturbed'], '../figs/fig3d.png')

    plotter.plot_xy_trajectory(plotter.df_ori['x1'], plotter.df_ori['y1'], plotter.df_ori['x2'], plotter.df_ori['y2'],
                               ['Inner Pendulum (1)', 'Outer Pendulum (2)'], '../figs/fig4a.png')
    plotter.plot_xy_trajectory(plotter.df_mod['x1'], plotter.df_mod['y1'], plotter.df_mod['x2'], plotter.df_mod['y2'],
                               ['Inner Pendulum (1)', 'Outer Pendulum (2)'], '../figs/fig4b.png')

    plotter.plot_phase_space(plotter.df_ori['theta1'], plotter.df_ori['omega1'], plotter.df_ori['theta2'],
                             plotter.df_ori['omega2'], ['Inner Pendulum (1)', 'Outer Pendulum (2)'],
                             '../figs/fig4c.png')
    plotter.plot_phase_space(plotter.df_mod['theta1'], plotter.df_mod['omega1'], plotter.df_mod['theta2'],
                             plotter.df_mod['omega2'], ['Inner Pendulum (1)', 'Outer Pendulum (2)'],
                             '../figs/fig4d.png')

