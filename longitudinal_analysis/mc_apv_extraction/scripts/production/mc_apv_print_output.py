#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2018/1/18
# Title: mc_apv_print_output.py
#
# Overview: Python script for calculating and printing the final uncertainties.
# =============================================================================

# Import necessary packages/modules
import argparse
import numpy as np
import pandas as pd

def load_data(path):
    return pd.read_csv(path, index_col=0)

def main():
    # Parse inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        type=str,
                        help='Enter path of apv extraction output .csv file.')
    inputs = parser.parse_args()
    
    # Load .csv file from given path
    df = load_data(inputs.path)

    # Test
    print(df.sort_values(by=['std'], ascending=False)['std'])

if __name__ == "__main__":
    main()
    exit()
