#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2017/12/4
#
# Python script for calculating Schwinger cross-section correction.
#
# Source: Eq.6-8c "Electron Scattering From Complex Nuclei" Herbert Uberall
# =============================================================================

import argparse
import numpy as np
from scipy.special import spence


def schwinger(energy, deltaE, theta, qq):
    '''Energy [MeV], delta [MeV], theta [deg], qq [MeV^2]'''
    alpha = 1/137.035999139  # Fine structure constant (2016 PDG)
    m_e = 0.5109989461  # Electron mass [MeV^2] (2016 PDG)

    term1 = np.log(energy/deltaE) - (13.0/12.0)
    term2 = np.log(qq/np.square(m_e)) - 1.0
    term3 = (17.0/36.0)
    spence_term = spence(1.0 - np.square(np.cos(np.deg2rad(theta)/2.0)))
    term4 = 0.5 * ((np.square(np.pi)/6.0) - spence_term)
    ds = 2.0*(alpha/np.pi) * (term1 * term2 + term3 + term4)
    return ds

if __name__ == '__main__':
    # Allow parsing of inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('energy',
                        type=float,
                        help='Enter initial energy [MeV].')
    parser.add_argument('deltaE',
                        type=float,
                        help='Enter delta E parameter [MeV].')
    parser.add_argument('theta',
                        type=float,
                        help='Enter theta value [deg].')
    parser.add_argument('qq',
                        type=float,
                        help='Enter Q^2 value [MeV^2].')

    inputs = parser.parse_args()
    ds = schwinger(inputs.energy,
                   inputs.deltaE,
                   inputs.theta,
                   inputs.qq)

    print('Schwinger Correction: {0}'.format(ds))

    exit()  # Close program.
