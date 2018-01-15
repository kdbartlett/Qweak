#!/usr/bin/bash

process="DWelastic quasi inelastic DWZn DWMg DWCu DWCr DWFe DWSi Mn Ti GDR pions 0844keV 1014keV 2211keV 2735keV 2990keV 4580keV 4812keV 5430keV 5668keV 7228keV 7477keV"

for label in $process
do
    grep -r -h "rates" sim_data/Al_Alloy_4p_DS_${label}_run1_QS_*_avg.dat > Al_Alloy_4p_DS_${label}_run1_sim_avg.csv
done
