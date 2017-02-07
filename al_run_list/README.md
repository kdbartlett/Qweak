#al_run_list
Python script for extracting run information from the Qweak mysql db into a csv file for future use.

##Requirements
The script requires the following python packages for operation: 

* python3
* PyMySQL
* PyYAML
* Pandas
* Numpy

##Usage
Pass the get_run_list.py executable the following parameters:

```bash
pytnon3 get_run_list.py <run#> <file.csv>
```
where <run#> is either `run1` or `run2` and file.csv is a .csv file of your choosing.
