#!/usr/bin/bash


#Declare arrays of possible inputs
run=(1 2)
target_type=('US-1%-Aluminum' 'US-2%-Aluminum' 'US-4%-Aluminum' 'DS-2%-Aluminum' 'DS-4%-Aluminum' 'DS-8%-Aluminum')
#Get number of elements in the array
run_elem=${#run[@]}
target_elem=${#target_type[@]}

for ((i=0;i<$run_elem;i++)); do
     for((ii=0;ii<$target_elem;ii++)); do
         python3 get_run_list.py run${run[${i}]} ${target_type[${ii}]} al_run${run[${i}]}_${target_type[${ii}]}.csv
     done
done

cat al_run1_US-*.csv al_run1_DS-*.csv | grep -v 'transverse' > al_run1_long.csv
cat al_run1_US-*.csv al_run1_DS-*.csv | grep 'transverse' > al_run1_trans.csv
cat al_run2_US-*.csv al_run2_DS-*.csv | grep -v 'transverse' > al_run2_long.csv
cat al_run2_US-*.csv al_run2_DS-*.csv | grep 'transverse' > al_run2_trans.csv
