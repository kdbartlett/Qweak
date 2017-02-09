# ==============================================================================
# Kurtis Bartlett
# 2017/2/7
#
# Created with help from Wade.
#
# !/usr/bin/env python3
# ==============================================================================


# Import necessary libraries/packages
import pymysql
import yaml
import csv
import sys
import pandas as pd
import numpy as np


# Function for connecting to sql db.
def connect_mysql(run_num):
    '''Read in yaml configuration file and return a connection using the data from the file.'''

    # Open connection and read it into directory
    with open('qweak_db_%s_read_cred.yml' % (run_num)) as f:
        mysql_db = yaml.safe_load(f)
        if mysql_db is None:
            raise Exception('Cannot open qweak_db_run#_read_cred.yml, config correct?')
    return pymysql.connect(**mysql_db)


# Temp function for sql query of interest
def sql_query(target):
    sql = "SELECT bm.run_number AS 'Run #', bm.slug AS 'Slug', bm.wien_slug AS 'Wien', sc.target_position AS 'Target', ROUND(MAX(bm.value),0) AS 'Beam Current', ROUND(MAX(sc.qtor_current),0) AS 'QTor Current', sc.wien_reversal AS 'Pol. State' ,sc.slow_helicity_plate AS 'IHWP1', sc.passive_helicity_plate AS 'IHWP2' FROM beam_view AS bm LEFT JOIN slow_controls_settings AS sc ON bm.runlet_id=sc.runlet_id WHERE sc.target_position='%s' AND bm.monitor='qwk_bcm6' AND bm.value > 0 GROUP BY bm.run_number" % (target)
    return sql

if __name__ == '__main__':

    # Open connection to database and create a cursor to pass around
    try:
        connection = connect_mysql(sys.argv[1])
    except pymysql.err.OperationalError:
        print('Failed to open connection to the database!')
    cursor = connection.cursor()

    # Pass the sql query function the slug range of interest
    query = sql_query(sys.argv[2])
    # print(query)
    # Execute query and collect all rows.
    cursor.execute(query)
    sql_result = cursor.fetchall()

    # Fetchall returns list of tuples,
    # throw into Pandas dataframe for quick export to csv.
    data = pd.DataFrame(np.asarray(sql_result))
    data.to_csv(sys.argv[3], index=False, header=False)
    # print(query)

    # Close connections
    cursor.close()
    connection.close
