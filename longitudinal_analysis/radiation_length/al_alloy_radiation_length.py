#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2017/12/1
#
# Python script for calculating the radiation length of the aluminum target
# alloy using Bragg's additivity rule.
#
# Source: Section 33.4.2 PDG 2016 "Passage of particles through matter"
# =============================================================================

# Import necessary packages/modules
import argparse
import numpy as np
import pandas as pd

if __name__ == "__main__":
    # Allow parsing of inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help='Enter location of .csv file')

    inputs = parser.parse_args()
    data = pd.read_csv(inputs.file)
    length = (np.sum(data.percentweight/data.radlength)) ** (-1)
    print('Calculated Radiation Length [g cm^-2]: {0:.4f}'.format(length))
    exit()  # Close program
