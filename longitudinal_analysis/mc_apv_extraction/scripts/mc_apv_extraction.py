#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2017/6/22
# mc_apv_extraction.py
# Python script for performing Monte Carlo/Many Worlds for determining and
# propogating uncertainty in Aluminum A_pv extraction
# =============================================================================

# Import necessart packages/modules
import argparse
import numpy as np

if __name__ == '__main__':
    # Allow parsing of inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Enter path of .csv input file')
    inputs = parser.parse_args()

    # Debug statement
    # print(inputs.path)
