#!/usr/bin/env python

"""
Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: May 3, 2024
File Name: shanon_ent.py

This script calculates Shannon Entropy from a simulated double pendulum system.
"""

import pandas as pd
import numpy as np

# Function to calculate Shannon entropy and save interpretations and scores
def calculate_and_save_entropy(df, save_path):
    entropy_results = {}
    interpretations = {}
    for col in df.columns:
        data = df[col]
        unique_values, value_counts = np.unique(data, return_counts=True)
        probabilities = value_counts / len(data)
        entropy_val = -np.sum(probabilities * np.log2(probabilities))
        entropy_results[col] = entropy_val
        if entropy_val <= 0.5:
            interpretations[col] = 'Low entropy: Predictable'
        elif entropy_val <= 1.0:
            interpretations[col] = 'Medium entropy: Some predictability'
        else:
            interpretations[col] = 'High entropy: Unpredictable'

    # Combine interpretations and scores
    result_df = pd.DataFrame.from_dict(entropy_results, orient='index', columns=['Entropy'])
    result_df['Interpretation'] = result_df['Entropy'].apply(lambda x: 'Low entropy: Predictable' if x <= 0.5
                                                              else 'Medium entropy: Some predictability' if x <= 1.0
                                                              else 'High entropy: Unpredictable')
    result_df['Entropy'] = result_df['Entropy'].map('{:.3f}'.format)  # Format to 3 decimal places

    # Save interpretations and scores in one file
    result_df.to_csv(f'{save_path}_entropy_scores_and_interpretations.csv')

if __name__ == "__main__":
    # Load the original time series data from a CSV file
    original_df = pd.read_csv('../data/python_double_pendulum_original.csv')

    # Load the perturbed time series data from a CSV file
    perturbed_df = pd.read_csv('../data/python_double_pendulum_modified.csv')

    # Calculate and save entropy for original data
    calculate_and_save_entropy(original_df, '../data/original')

    # Calculate and save entropy for perturbed data
    calculate_and_save_entropy(perturbed_df, '../data/perturbed')

