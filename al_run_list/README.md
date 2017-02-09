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
python3 get_run_list.py <run#> <slug#_low> <slug#_high> <file.csv>
```
where run# is either `run1` or `run2`, slug# is the lower and upper bound on the slug range and file.csv is the name of a .csv file of your choosing.

##Additional Notes
Included bash script for easy extraction of data from a variety of input parameters to the python code. Attempting to keep python script modular enough for possible future reuse with modification to allow passing of any sql query.  
