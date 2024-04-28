# ******************************************************************************
# Author: Sandy Herho <sandy.herho@email.ucr.edu>
# Date: April 28, 2024
# File Name: doublePendulumCalc.R
#
# Description:
#   This script simulates a double pendulum system using numerical integration
#   and saves the results to CSV files.
#
# Dependencies:
#   - Requires the 'deSolve' package for numerical integration.
#
# ******************************************************************************

# Load necessary libraries
library(deSolve)

# Define the differential equations for the double pendulum system
double_pendulum <- function(t, y, parms) {
  m1 <- parms$m1
  m2 <- parms$m2
  L1 <- parms$L1
  L2 <- parms$L2
  g <- parms$g
  
  a <- (m1 + m2) * L1
  b <- m2 * L2 * cos(y[1] - y[3])
  c <- m2 * L1 * cos(y[1] - y[3])
  d <- m2 * L2
  
  e <- -m2 * L2 * y[4]^2 * sin(y[1] - y[3]) - g * (m1 + m2) * sin(y[1])
  f <- m2 * L1 * y[2]^2 * sin(y[1] - y[3]) - m2 * g * sin(y[3])
  
  dy <- rep(0.0, 4)
  dy[1] <- y[2]
  dy[2] <- (e * d - b * f) / (a * d - c * b)
  dy[3] <- y[4]
  dy[4] <- (a * f - c * e) / (a * d - c * b)
  
  return(list(dy))
}

# Function to simulate the double pendulum and save results to a CSV file
simulate_double_pendulum <- function(m1, m2, L1, L2, g, initial_conditions, filename) {
  time_span <- c(0, 10)
  num_points <- 10000
  parms <- list(m1 = m1, m2 = m2, L1 = L1, L2 = L2, g = g)
  
  sol <- ode(y = initial_conditions, times = seq(time_span[1], time_span[2], length.out = num_points), func = double_pendulum, parms = parms)
  
  # Calculate x1, y1, x2, y2 based on theta1 and theta2
  x1 <- L1 * sin(sol[, 2])
  y1 <- -L1 * cos(sol[, 2])
  x2 <- x1 + L2 * sin(sol[, 4])
  y2 <- y1 - L2 * cos(sol[, 4])
  
  # Create the data frame with the correct structure
  data <- data.frame(
    t = sol[, 1],
    x1 = x1,
    y1 = y1,
    x2 = x2,
    y2 = y2,
    theta1 = sol[, 2],
    theta2 = sol[, 4],
    omega1 = sol[, 3],
    omega2 = sol[, 5]
  )
  
  write.csv(data, file = filename, row.names = FALSE)
}

# Function to run simulations for both original and modified double pendulum systems
run_double_pendulum_simulations <- function() {
  m1 <- 2
  m2 <- 1
  L1 <- 2
  L2 <- 1
  g <- 9.8
  
  initial_conditions_original <- c(pi, 0.0, 1.57, 0.0)
  initial_conditions_modified <- c(pi, 0.001, 1.57, 0.001)
  
  simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions_original, 'r_double_pendulum_original.csv')
  simulate_double_pendulum(m1, m2, L1, L2, g, initial_conditions_modified, 'r_double_pendulum_modified.csv')
}

# Run the simulations
run_double_pendulum_simulations()
