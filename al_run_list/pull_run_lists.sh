#!/usr/bin/bash


#Declare arrays of possible inputs
run=(1 2)
slug_low=(1000 2000 6000 101000 201000 501000)
slug_high=(2000 3000 7000 102000 202000 502000)
file_type=(long_DS4%_elastic long_US2%_elastic long_US2%_elastic trans_DS4%_vertical trans_DS4%_horizontal long_DS4%_ntodelta)
#Get number of elements in the array
run_elem=${#run[@]}
slug_elem=${#slug_low[@]}

for ((i=0;i<$run_elem;i++)); 
do
	for((ii=0;ii<$slug_elem;ii++));
	do
		python3 get_run_list.py run${run[${i}]} ${slug_low[${ii}]} ${slug_high[${ii}]} al_run${run[${i}]}_${file_type[${ii}]}.csv
	done
done
