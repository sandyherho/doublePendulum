#!/usr/bin/env python

"""
Author: Sandy Herho <sandy.herho@email.ucr.edu>
Date: May 3, 2024
File Name: exec_mem.py

This script calculates the difference between execution times & memory usages for each computing environment.
"""


import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import seaborn as sns
import matplotlib.pyplot as plt

# Set plot style
plt.style.use('bmh')


def analyze_and_compare_logs(log_paths, stat_path, fig_path, metric_name, labels):
  """
  Analyzes and compares runtime or memory usage from log files.

  Args:
    log_paths: List of paths to CSV log files.
    stat_path: Path to save descriptive statistics (CSV).
    fig_path: Path to save the boxplot figure (PNG).
    metric_name: Column name containing the metric (e.g., "runtime", "memory").
    labels: List of labels for the computing environments.

  Returns:
    None
  """

  # Read dataframes from log files
  dataframes = [pd.read_csv(path) for path in log_paths]

  # Descriptive statistics (rounded to 3 decimals)
  for df, label in zip(dataframes, labels):
    df[metric_name].describe().round(3).to_csv(f"{stat_path}/{label}.csv")

  # Combine data for Dunn's test
  all_data = [df[metric_name] for df in dataframes]
  data_stacked = np.concatenate(all_data)
  groups = np.concatenate([[label] * len(data) for data, label in zip(all_data, labels)])
  df_dunn = pd.DataFrame({'Execution Time': data_stacked, 'Group': groups})

  # Boxplot visualization
  plt.figure(figsize=(10, 6))
  sns.boxplot(x='Group', y=metric_name, data=df_dunn)
  plt.xticks(ticks=np.arange(len(labels)), labels=labels, fontsize=12)
  plt.yticks(fontsize=12)
  plt.xlabel('Computing Environment', fontsize=18)
  plt.ylabel(f"{metric_name} [seconds/MB]", fontsize=18)
  plt.tight_layout()
  plt.savefig(fig_path, dpi=450)

  # Kruskal-Wallis test
  alpha = 0.05
  kw_stat, kw_pvalue = stats.kruskal(*all_data)

  print(f'Kruskal-Wallis test statistic for {metric_name}: {kw_stat:.3f}, p-value: {kw_pvalue:.3f}')

  if kw_pvalue < alpha:
    print(f"Significant differences found among the groups for {metric_name}.")
    print("This indicates that at least one group's median significantly differs from the others.")
  else:
    print(f"No significant differences found among the groups for {metric_name}.")
    print("This suggests that there is no statistical evidence to conclude that the groups differ in median.")

  # Dunn's post-hoc test (if significant differences found)
  if kw_pvalue < alpha:
    dunn_pvalues = sp.posthoc_dunn(df_dunn, val_col=metric_name, group_col='Group', p_adjust='bonferroni')

    print(f"Dunn's test p-values (Bonferroni adjusted) for {metric_name}:")
    print(dunn_pvalues.round(3))
    print("Values below 0.05 indicate pairs of groups with statistically significant differences in medians.")


if __name__ == "__main__":
  # Define file paths and labels
  log_paths_runtime = [
      "../data/logs/py_log.csv",
      "../data/logs/m_log.csv",
      "../data/logs/jl_log.csv",
      "../data/logs/R_log.csv"
  ]
  log_paths_memory = [path.replace("runtime", "memory") for path in log_paths_runtime]
  stat_path_runtime = "../data/stats_run"
  stat_path_memory = stat_path_runtime.replace("runtime", "memory")
  fig_path_runtime = "../figs/fig2a.png"
  fig_path_memory = "../figs/fig2b.png"

