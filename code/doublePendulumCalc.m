%{
Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: April 28, 2024
File Name: doublePendulumCalc.m

This script simulates a double pendulum system in Octave and saves the results to CSV files.
%}

% Simulate the double pendulum system and save results to CSV
function simulate_double_pendulum()
    m1 = 2;
    m2 = 1;
    L1 = 2;
    L2 = 1;
    g = 9.8;

    % Define the double pendulum differential equations
    function dydt = double_pendulum_eq(t, y)
        a = (m1 + m2) * L1;
        b = m2 * L2 * cos(y(1) - y(3));
        c = m2 * L1 * cos(y(1) - y(3));
        d = m2 * L2;

        e = -m2 * L2 * y(4)^2 * sin(y(1) - y(3)) - g * (m1 + m2) * sin(y(1));
        f = m2 * L1 * y(2)^2 * sin(y(1) - y(3)) - m2 * g * sin(y(3));

        dydt = [
            y(2);
            (e * d - b * f) / (a * d - c * b);
            y(4);
            (a * f - c * e) / (a * d - c * b);
        ];
    endfunction

    % Initial conditions
    initial_conditions_original = [pi; 0.0; 1.57; 0.0];
    initial_conditions_modified = [pi; 0.001; 1.57; 0.001];

    % Time span and options for ODE solver
    tspan = [0, 10];
    options = odeset('RelTol', 1e-6, 'AbsTol', 1e-9);

    % Solve the ODEs for original and modified initial conditions
    [t_orig, y_orig] = ode45(@(t, y) double_pendulum_eq(t, y), tspan, initial_conditions_original, options);
    [t_mod, y_mod] = ode45(@(t, y) double_pendulum_eq(t, y), tspan, initial_conditions_modified, options);

    % Calculate positions
    x1_orig = L1 * sin(y_orig(:, 1));
    y1_orig = -L1 * cos(y_orig(:, 1));
    x2_orig = L1 * sin(y_orig(:, 1)) + L2 * sin(y_orig(:, 3));
    y2_orig = -L1 * cos(y_orig(:, 1)) - L2 * cos(y_orig(:, 3));

    x1_mod = L1 * sin(y_mod(:, 1));
    y1_mod = -L1 * cos(y_mod(:, 1));
    x2_mod = L1 * sin(y_mod(:, 1)) + L2 * sin(y_mod(:, 3));
    y2_mod = -L1 * cos(y_mod(:, 1)) - L2 * cos(y_mod(:, 3));

    % Save data to CSV files
    data_orig = [t_orig, x1_orig, y1_orig, x2_orig, y2_orig, y_orig(:, 1), y_orig(:, 3), y_orig(:, 2), y_orig(:, 4)];
    data_mod = [t_mod, x1_mod, y1_mod, x2_mod, y2_mod, y_mod(:, 1), y_mod(:, 3), y_mod(:, 2), y_mod(:, 4)];

    csvwrite('../data/octave_double_pendulum_original.csv', data_orig);
    csvwrite('../data/octave_double_pendulum_modified.csv', data_mod);
endfunction

% Run the simulations
simulate_double_pendulum();

