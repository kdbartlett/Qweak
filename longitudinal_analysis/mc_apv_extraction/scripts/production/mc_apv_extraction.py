#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2018/1/17
# Title: mc_apv_extraction.py (Updated technique)
#
# Overview: Python script for performing Monte Carlo/Many Worlds calculation
# for determining and propogating uncertainty in the Aluminum A_pv extraction.
#
# Usage: Requires a three column input .csv file containting the names, values,
# and uncertainty of all of the inputs to the Aluminum A_pv extraction formula.
#
# ./mc_apv_extraction.py "path to input data(.csv)" "num of samples(int)"
# =============================================================================

# Import necessary packages/modules
import argparse
import pandas as pd
import numpy as np
from scipy.stats import norm
import multiprocessing
import matplotlib as mpl
mpl.use('pgf')


def figsize(scale):
    '''Calculate LaTex figure scale.'''
    fig_width_pt = 433.62001
    inches_per_pt = 1.0/72.0
    golden_mean = (np.sqrt(5.0)-1.0)/2.0
    fig_width = fig_width_pt*inches_per_pt*scale
    fig_height = fig_width*golden_mean
    fig_size = [fig_width, fig_height]
    return fig_size


pgf_with_lualatex = {
    "pgf.texsystem": "lualatex",
    "text.usetex": True,
    "pgf.rcfonts": False,
    "font.family": "serif",
    "font.serif": "Computer Modern Roman",
    # "font.sans-serif": "Computer Modern Sans serif",
    # "font.serif": [],
    "font.sans-serif": [],
    "font.monospace": [],
    # Text size
    "font.size": 11,
    # "text.fontsize": 11,
    "axes.labelsize": 11,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    # Axis
    # "axes.labelpad": 2,
    "figure.figsize": figsize(1.0),
    # Packages
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}"]
    }

mpl.rcParams.update(pgf_with_lualatex)

# Now load pyplot package after mpl setup.
import matplotlib.pyplot as pp
import seaborn as sns

pp.style.use('seaborn-ticks')


def load_data(loc):
    '''Pass directory path of input (string), returns DataFrame.'''
    return np.transpose(pd.read_csv(loc, header=None, index_col=0))


def construct_map(name):
    '''Construct name map of DataFrame columns.'''
    nmap = np.full((len(name), len(name)), list(name), dtype='<U16')
    for i in range(len(name)):
        nmap[i][i] = 'rand_' + nmap[i][i]
    return nmap


def randomize_data(data, samples):
    '''Generates new DataFrame w/o randmized (Gaussian) inputs from input.'''
    rand_data = pd.DataFrame()
    for label in data.columns:
        rand_data[label] = data[label][1]*np.ones(samples)
        if data[label][2] != 0.0:
            rand_data['rand_' + label] = np.random.normal(data[label][1],
                                                          data[label][2],
                                                          samples)
        else:
            rand_data['rand_' + label] = rand_data[label]
    return rand_data


def calculate_asym(df, nrow):
    '''Calculate elastic aluminum A_pv.'''
    A_msr = np.divide((df[nrow[0]]
                       + df[nrow[1]]
                       + df[nrow[2]]
                       + df[nrow[3]]
                       + df[nrow[4]]
                       + df[nrow[5]]
                       + df[nrow[6]]), df[nrow[7]])

    fA = ((df[nrow[32]] * df[nrow[8]])
          + (df[nrow[33]] * df[nrow[9]])
          + (df[nrow[34]] * df[nrow[10]])
          + (df[nrow[35]] * df[nrow[11]])
          + (df[nrow[36]] * df[nrow[12]])
          + (df[nrow[37]] * df[nrow[13]])
          + (df[nrow[38]] * df[nrow[14]])
          + (df[nrow[39]] * df[nrow[15]])
          + (df[nrow[40]] * df[nrow[16]])
          + (df[nrow[41]] * df[nrow[17]])
          + (df[nrow[42]] * df[nrow[18]])
          + (df[nrow[43]] * df[nrow[19]])
          + (df[nrow[44]] * df[nrow[20]])
          + (df[nrow[45]] * df[nrow[21]])
          + (df[nrow[46]] * df[nrow[22]])
          + (df[nrow[47]] * df[nrow[23]])
          + (df[nrow[48]] * df[nrow[24]])
          + (df[nrow[49]] * df[nrow[25]])
          + (df[nrow[50]] * df[nrow[26]])
          + (df[nrow[51]] * df[nrow[27]])
          + (df[nrow[52]] * df[nrow[28]])
          + (df[nrow[53]] * df[nrow[29]])
          + (df[nrow[54]] * df[nrow[30]])
          + (df[nrow[55]] * df[nrow[31]]))

    f = (df[nrow[32]]
         + df[nrow[33]]
         + df[nrow[34]]
         + df[nrow[35]]
         + df[nrow[36]]
         + df[nrow[37]]
         + df[nrow[38]]
         + df[nrow[39]]
         + df[nrow[40]]
         + df[nrow[41]]
         + df[nrow[42]]
         + df[nrow[43]]
         + df[nrow[44]]
         + df[nrow[45]]
         + df[nrow[46]]
         + df[nrow[47]]
         + df[nrow[48]]
         + df[nrow[49]]
         + df[nrow[50]]
         + df[nrow[51]]
         + df[nrow[52]]
         + df[nrow[53]]
         + df[nrow[54]]
         + df[nrow[55]]
         + df[nrow[56]])  # Beamline Background

    R = (df[nrow[57]]
         * df[nrow[58]]
         * df[nrow[59]]
         * df[nrow[60]])

    A_pv = R * np.divide((A_msr-fA), (np.ones(len(df))-f))
    return A_pv


def calculate_stats(df):
    mean = [np.mean(df[label]) for label in df.columns]
    std = [np.std(df[label]) for label in df.columns]
    return pd.DataFrame([mean, std], columns=df.columns, index=['mean', 'std'])


def plot_distribution(label, data):
    pp.figure(figsize=figsize(1))
    ax = sns.distplot(data,
                      kde=True,
                      fit=norm,
                      norm_hist=True)
    pp.savefig('plots/mc_apv_' + label + '_distribution.png',
               bbox_inches='tight')


def plot_uncertainties(names, uncert):
    bar_range = np.arange(0.0, len(uncert))
    pp.figure(figsize=(20, 4))
    pp.bar(bar_range, uncert)
    pp.xticks(bar_range, names, rotation=90, horizontalalignment='center')
    pp.savefig('plots/mc_apv_uncertainty_chart.png',
               bbox_inches='tight')


def main():
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        type=str,
                        help='Enter path of input .csv file.')
    parser.add_argument('samples',
                        type=int,
                        help='Enter number of Monte Carlo samples (int only).')
    inputs = parser.parse_args()

    # Load .csv file from given input path.
    df = load_data(inputs.path)

    # Construct naming map
    name = construct_map(df.columns)

    # Randomize data
    rand = pd.DataFrame()  # Empty frame to fill.
    rand = randomize_data(df, inputs.samples)

    # Calculate all combinations
    results = pd.DataFrame()  # Empty frame to fill.
    for i in range(len(name)):
        results[np.diag(name)[i][5:]] = calculate_asym(rand, name[i])
    results['A_pv'] = calculate_asym(rand, np.diag(name))
    results['CV'] = calculate_asym(rand, df.columns)

    # Calculate stats(mean, std).
    results_stats = calculate_stats(results)
    np.transpose(results_stats).to_csv('mc_apv_extraction_output.csv')

    # Test
    #plot_distribution('A_pv', results['A_pv'])
    #plot_uncertainties(results_stats.columns, results_stats.loc['std'])


if __name__ == '__main__':
    main()
    exit()
