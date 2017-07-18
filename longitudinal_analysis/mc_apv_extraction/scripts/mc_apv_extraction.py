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
import pandas as pd
import numpy as np


def calculate_apv(A_msr, R, asym, frac):
    '''Calculate A_pv'''

    # Calculate the A_msr/P ratio
    A_msr_pol = (A_msr +
                 asym.A_reg +
                 asym.A_nonlin +
                 asym.A_Q +
                 asym.A_beamline +
                 asym.A_bias) / asym.P

    # Calculate numerator
    A_num = A_msr_pol - (asym.f_neutral * asym.A_neutral +
                         frac.f_quasi * asym.A_quasi +
                         frac.f_inelastic * asym.A_inelastic +
                         frac.f_844keV * asym.A_844keV +
                         frac.f_1014keV * asym.A_1014keV +
                         frac.f_2211keV * asym.A_2211keV +
                         frac.f_2735keV * asym.A_2735keV +
                         frac.f_2990keV * asym.A_2990keV +
                         frac.f_4580keV * asym.A_4580keV +
                         frac.f_4812keV * asym.A_4812keV +
                         frac.f_5430keV * asym.A_5430keV +
                         frac.f_5668keV * asym.A_5668keV +
                         frac.f_7228keV * asym.A_7228keV +
                         frac.f_7477keV * asym.A_7477keV +
                         frac.f_GDR * asym.A_GDR +
                         frac.f_Zn * asym.A_Zn +
                         frac.f_Mg * asym.A_Mg +
                         frac.f_Cu * asym.A_Cu +
                         frac.f_Cr * asym.A_Cr +
                         frac.f_Fe * asym.A_Fe +
                         frac.f_Si * asym.A_Si +
                         frac.f_Mn * asym.A_Mn +
                         frac.f_Ti * asym.A_Ti)

    # Calculate denominator
    A_denom = 1.0 - (asym.f_beamline +
                     asym.f_neutral +
                     frac.f_quasi +
                     frac.f_inelastic +
                     frac.f_844keV +
                     frac.f_1014keV +
                     frac.f_2211keV +
                     frac.f_2735keV +
                     frac.f_2990keV +
                     frac.f_4580keV +
                     frac.f_4812keV +
                     frac.f_5430keV +
                     frac.f_5668keV +
                     frac.f_7228keV +
                     frac.f_7477keV +
                     frac.f_GDR +
                     frac.f_Zn +
                     frac.f_Mg +
                     frac.f_Cu +
                     frac.f_Cr +
                     frac.f_Fe +
                     frac.f_Si +
                     frac.f_Mn +
                     frac.f_Ti)
    # Calculate the parity-violating physics asymmetry
    A_pv = R * (A_num / A_denom)
    return A_pv


def gaussian(value, n):
    '''Return list containing n amount of normally distributed values'''
    return np.random.normal(value[0], value[1], n)


def one_vec(value, n):
    return value*np.ones(n)

if __name__ == '__main__':
    # Allow parsing of inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('corr_path',
                        type=str,
                        help='Enter path of asym correction input .csv file')
    parser.add_argument('bk_frac_path',
                        type=str,
                        help='Enter path of bk fraction input .csv file')
    parser.add_argument('output_path',
                        type=str,
                        help='Enter path for .csv output file')
    inputs = parser.parse_args()

    # Load asymmetry corrections
    try:
        asym_corr = pd.read_csv(inputs.corr_path)
    except Error as e:
        print(e)

    # Load normally distributed background fractions
    try:
        bk_fractions = pd.read_csv(inputs.bk_frac_path)
    except Error as e:
        print(e)

    # Number of samples
    n = len(bk_fractions)

    # New dataframe for randomized asym corrections
    asym = pd.DataFrame()

    # New dataframe for calculated Asymmetries and Errors
    cal_asym = pd.DataFrame()

    # Pull columns labels from asym_corr
    # Remove A_msr from list
    asym_cols = asym_corr.columns[1:]

    # Generator vector of A_msr
    a_msr = one_vec(asym_corr.A_msr[0], n)
    a_stat = asym_corr.A_msr[1] / asym_corr.A_msr[0]  # [rel.]
    # Temp R variable - KDB
    r = one_vec(1.0, n)

    # Fill asym dataframe with normally distributed values
    # Sample the same number as bk_fractions
    for col in asym_cols:
        asym[col] = gaussian(asym_corr[col], n)

    # Write asymmetry corrections to .csv file
    asym.to_csv(inputs.output_path,
                index=False,
                mode='w',
                float_format='%.6f')

    # Add calculated A_pv to cal asym dataframe
    cal_asym['A_pv'] = calculate_apv(a_msr, r, asym, bk_fractions)

    # Print out results
    print('    Mean: {0:.4f}\n'.format(cal_asym.A_pv.mean()) +
          ' Sys Err: {0:.4f}\n'.format(cal_asym.A_pv.std()) +
          'Stat Err: {0:.4f}\n'.format(a_stat*cal_asym.A_pv.mean()))

    # Write calculated asymmetry to .csv file
    cal_asym.to_csv(inputs.output_path[:-4] + '_cal' inputs.output_path[-4:],
                    index=False,
                    mode='w',
                    float_format='%.6f')
    exit()
