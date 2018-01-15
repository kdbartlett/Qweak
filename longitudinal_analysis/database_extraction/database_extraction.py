#!/usr/bin/env python3
# ==============================================================================
# Kurtis Bartlett
# 2017/8/16
#
# Python script for connecting to Qweak SQL database, passing desired query,
# returning all rows from query in a .csv file. Created with help from Wade.
#
# ==============================================================================


# Import necessary packages/modules
import argparse
import pymysql
import yaml
import csv
import sys
import pandas as pd
import numpy as np


# Function for connecting to sql db.
def connect_mysql(run_num):
    """
    Read in yaml configuration file,
    then return a connection using the data from the file.
    """

    # Open connection and read it into directory
    with open('qweak_db_run%s_read_cred.yml' % (run_num)) as f:
        mysql_db = yaml.safe_load(f)
        if mysql_db is None:
            raise Exception('Cannot open qweak_db_run#_read_cred.yml!')
    return pymysql.connect(**mysql_db)

if __name__ == '__main__':
    # Allow parsing of inputs.
    parser = argparse.ArgumentParser()
    parser.add_argument('run_num', type=int,
                        help='Enter Run number')
    parser.add_argument('query', type=str,
                        help='Enter valid sql query file.')
    parser.add_argument('file_name', type=str,
                        help='Enter name of .csv file.')
    inputs = parser.parse_args()

    # Open connection to database and create a cursor to pass around
    try:
        connection = connect_mysql(inputs.run_num)
    except pymysql.err.OperationalError:
        print('Failed to open connection to the database!')
    cursor = connection.cursor()

    # Open .sql file
    query_file = open(inputs.query, 'r')
    query = query_file.read()
    query_file.close()

    # Execute query and collect all rows.
    cursor.execute(query)
    sql_result = cursor.fetchall()

    # Fetchall returns list of tuples,
    # throw into Pandas dataframe for quick export to csv.
    data = pd.DataFrame(np.asarray(sql_result))
    data.to_csv(inputs.file_name, index=False, header=False)

    # Close connections
    cursor.close()
    connection.close
