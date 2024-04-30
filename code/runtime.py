#!/usr/bin/env python

import csv
import subprocess
import time
import os
import resource

# Function to run the script and measure runtime and memory usage
def run_script(script_path, command):
    start_time = time.time()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    end_time = time.time()
    runtime = end_time - start_time

    # Get memory usage using resource module
    mem_usage = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024  # Convert to MB

    return runtime, mem_usage

# Function to save data to CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['runtime', 'memory'])
        writer.writerows(data)

if __name__ == "__main__":
    # Number of runs
    num_runs = 999

    # Script paths and commands
    scripts = [
        #{'path': 'doublePendulumCalc.py', 'command': 'python doublePendulumCalc.py'},
        #{'path': 'doublePendulumCalc.R', 'command': 'Rscript doublePendulumCalc.R'},
        #{'path': 'doublePendulumCalc.m', 'command': 'octave-cli doublePendulumCalc.m'},
        {'path': 'doublePendulumCalc.jl', 'command': 'julia doublePendulumCalc.jl'}
    ]

    # Create the data directory if it doesn't exist
    data_dir = '../data/logs/'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Run each script and log runtime and memory usage
    for script in scripts:
        data = []
        for _ in range(num_runs):
            runtime, mem_usage = run_script(script['path'], script['command'])
            data.append([runtime, mem_usage])

        # Save data to CSV file
        language = script['path'].split('.')[1]  # Get the programming language from the script file extension
        filename = f'{data_dir}{language}_log.csv'
        save_to_csv(data, filename)

        print(f'{language} log saved to {filename}')

