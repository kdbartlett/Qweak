#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2017/6/22
# mc_background_fraction_calculation.py
# Python script for performing Monte Carlo/Many Worlds for determining and
# propogating uncertainty in Aluminum A_pv background fraction calculation.
# =============================================================================

# Import necessary packages/modules
import argparse
import pandas as pd
import numpy as np


def gaussian(value, n):
    '''Return list containing n amount of normally distributed values'''
    return np.random.normal(value[0], value[1], n)

if __name__ == '__main__':
    # Allow parsing of inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path',
                        type=str,
                        help='Enter path of .csv input file.')
    parser.add_argument('-n', type=float, help='Number of samples.')
    parser.add_argument('output_path',
                        type=str,
                        help='Enter path for .csv output file.')
    inputs = parser.parse_args()

    # Load data from .csv into Pandas dataframe.
    try:
        input_data = pd.read_csv(inputs.input_path)
    except Error as e:
        print(e)

    # Pull list names from column headers
    yield_names = list(input_data.columns)
    frac_names = [char.replace('y', 'f') for char in yield_names]
    # New dataframe for randomized yields
    yields = pd.DataFrame()

    # Fill fractions dataframe with normally distributed values
    for col in yield_names:
        yields[col] = gaussian(input_data[col], int(inputs.n))

    # Calculate total yield
    yields['y_total'] = yields.sum(axis=1)

    # New dataframe for calculated fractions
    fractions = pd.DataFrame()

    # Interation var
    i = 0

    # Calculate background fractions
    for col in yield_names:
        fractions[frac_names[i]] = yields[col]/yields['y_total']
        i += 1

    means = [fractions[col].mean() for col in frac_names]
    errors = [fractions[col].std() for col in frac_names]

    output_data = pd.DataFrame([means,errors],
                                columns=frac_names,
                                index=['means', 'errors'])
    output_data.to_csv(inputs.output_path, mode='w')
    exit()
