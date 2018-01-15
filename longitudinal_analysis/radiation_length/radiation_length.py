#!/usr/bin/env python3
# =============================================================================
# Kurtis Bartlett
# 2017/11/30
#
# Python script for calculating radiation lengths of given element.
#
# Source: Section 33.4.2 PDG 2016 "Passage of particles through matter"
# =============================================================================

# Import necessary packages/modules
import argparse
import numpy as np


def radiation_length(Z, A):
    """
    Calculate radation length of element, takes atomic number and atomic mass
    in units of [g mol^-1]
    """

    alpha = 1/137.035999139  # Fine struction constant (PDG 2016)
    r_e = 2.8179403227e-15  # [m] Classical electron radius (PDG 2016)
    N_A = 6.0222140857e23  # [mol^-1] Avogadro constant (PDG 2016)

    term = (L_rad(Z) - f(Z)) * Z**2 + Z * L_radp(Z)
    return (4.0 * alpha * (r_e * 100) ** (2) * (N_A/A) * (term)) ** (-1)


def L_rad(Z):
    if Z == 1:
        lrad = 5.31
    elif Z == 2:
        lrad = 4.79
    elif Z == 3:
        lrad = 4.74
    elif Z == 4:
        lrad = 4.71
    elif Z > 4:
        lrad = np.log(184.15 * Z ** (-1 / 3))
    else:
        print("Err L_rad function: Enter valid value for atomic number (Z).")
    return lrad


def L_radp(Z):
    if Z == 1:
        lradp = 6.144
    elif Z == 2:
        lradp = 5.621
    elif Z == 3:
        lradp = 5.805
    elif Z == 4:
        lradp = 5.924
    elif Z > 4:
        lradp = np.log(1194 * Z ** (-2 / 3))
    else:
        print("Err L_radp function: Enter valid value for atomic number (Z).")
    return lradp


def f(Z):
    """
    Infinite sum function, valid up to Uranium (Z=92) and to 4 decimal places.
    """

    alpha = 1/137.035999139  # Fine struction constant (PDG 2016)

    a = alpha * Z

    term1 = (1 + a ** (2)) ** (-1)
    term2 = 0.20206
    term3 = -0.0369 * a ** (2)
    term4 = 0.0083 * a ** (4)
    term5 = -0.002 * a ** (6)

    return a ** (2) * (term1 + term2 + term3 + term4 + term5)

if __name__ == '__main__':
    # Allow parsing of inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('Z', type=int, help='Enter atomic number of element.')
    parser.add_argument('A', type=float,
                        help='Enter atomic mass in units of [g mol^(-1)]')

    inputs = parser.parse_args()

    length = radiation_length(inputs.Z, inputs.A)

    print('Inputs:')
    print('Z: {0}     A:{1:}\n'.format(inputs.Z, inputs.A))
    print('Calculated Radiation Length:')
    # print('Test: f(Z) {0}'.format(f(inputs.Z)))
    print('X_0 [g cm^(-2)]: {0:.4f}'.format(length))

    exit()  # Close program
