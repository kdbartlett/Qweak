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
python3 get_run_list.py <run#> <target> <file.csv>
```
where run# is either `run1` or `run2`, target is the type you want to select on, and file.csv is the name of a .csv file of your choosing.

###List of possible aluminum targets
Use exact text given at each bullet:
* US-1%-Aluminum
* US-2%-Aluminum
* US-4%-Aluminum
* DS-2%-Aluminum
* DS-4%-Aluminum
* DS-8%-Aluminum

##Additional Notes
Included bash script for easy extraction of data from a variety of input parameters to the python code. Attempting to keep python script modular enough for possible future reuse with modification to allow passing of any sql query.  
