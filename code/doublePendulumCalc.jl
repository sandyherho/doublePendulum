#=
Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: April 28, 2024
File Name: doublePendulumCalc.jl

This script simulates a double pendulum system in Julia and saves the results to CSV files.
=#

using DifferentialEquations, CSV, DataFrames

function double_pendulum!(du, u, p, t)
    m1, m2, L1, L2, g = p

    a = (m1 + m2) * L1
    b = m2 * L2 * cos(u[1] - u[3])
    c = m2 * L1 * cos(u[1] - u[3])
    d = m2 * L2

    e = -m2 * L2 * u[4]^2 * sin(u[1] - u[3]) - g * (m1 + m2) * sin(u[1])
    f = m2 * L1 * u[2]^2 * sin(u[1] - u[3]) - m2 * g * sin(u[3])

    du[1] = u[2]
    du[2] = (e * d - b * f) / (a * d - c * b)
    du[3] = u[4]
    du[4] = (a * f - c * e) / (a * d - c * b)
end

function simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions, filename)
    tspan = (0.0, 10.0)
    prob = ODEProblem(double_pendulum!, initial_conditions, tspan, [m1, m2, L1, L2, g])
    sol = solve(prob, Vern7(), saveat=0.001)

    t = sol.t
    x1 = L1 * sin.(sol[1, :])
    y1 = -L1 * cos.(sol[1, :])
    x2 = L1 * sin.(sol[1, :]) + L2 * sin.(sol[3, :])
    y2 = -L1 * cos.(sol[1, :]) - L2 * cos.(sol[3, :])
    theta1 = sol[1, :]
    theta2 = sol[3, :]
    omega1 = sol[2, :]
    omega2 = sol[4, :]

    df = DataFrame(t=t, x1=x1, y1=y1, x2=x2, y2=y2, theta1=theta1, theta2=theta2, omega1=omega1, omega2=omega2)
    CSV.write(filename, df)
end

function run_double_pendulum_simulations()
    m1 = 2
    m2 = 1
    L1 = 2
    L2 = 1
    g = 9.8

    initial_conditions_original = [π, 0.0, 1.57, 0.0]
    initial_conditions_modified = [π, 0.001, 1.57, 0.001]

    simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions_original, "../data/julia_double_pendulum_original.csv")
    simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions_modified, "../data/julia_double_pendulum_modified.csv")
end

if abspath(PROGRAM_FILE) == @__FILE__
    run_double_pendulum_simulations()
end

