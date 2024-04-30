#!/usr/bin/env python

import pandas as pd
from scipy.stats import ks_2samp

def perform_ks_test():
    # Load the original time series data from a CSV file
    original_df = pd.read_csv('../data/python_double_pendulum_original.csv')

    # Load the perturbed time series data from a CSV file
    perturbed_df = pd.read_csv('../data/python_double_pendulum_modified.csv')

    # Columns in the CSV files
    columns = original_df.columns

    # Perform Kolmogorov-Smirnov test
    results = []
    for col in columns:
        original_data = original_df[col].values
        perturbed_data = perturbed_df[col].values

        # Compute the Kolmogorov-Smirnov statistic
        statistic, p_value = ks_2samp(original_data, perturbed_data)

        # Interpret the K-S test result
        alpha = 0.05  # Significance level (you can change this as needed)
        if p_value < alpha:
            interpretation = "Distributions are different (reject null hypothesis)"
        else:
            interpretation = "Distributions are similar (fail to reject null hypothesis)"

        # Append the results to the list
        results.append([col, statistic, p_value, interpretation])

    # Save the results to a CSV file
    results_df = pd.DataFrame(results, columns=['Variable', 'KS_Statistic', 'p_value', 'Interpretation'])
    results_df.to_csv('../data/ks_test_results.csv', index=False)

if __name__ == "__main__":
    perform_ks_test()
