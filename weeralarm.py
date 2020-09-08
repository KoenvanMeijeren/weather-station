#!/usr/bin/python3

#
# NAME
#   weeralarm.py - script which alarms when temperature above a threshold
#
# SYNOPSIS
#   weeralarm.py [-v] [-t interval] [-T threshold]
#       -v: verbose
#       -t interval: sample every interval seconds
#       -T threshold: alarm above this value
#
# DESCRIPTION
#   reads temperatures fromSQL database and colors 8x8 LED display
#

# import some modules
import sys
import getopt
import sense_hat
import time
import mysql.connector as mariadb
from mysql.connector import errorcode

# sensor name
sensor_name = 'Temperatuur'

# database connection configuration
dbconfig = {
    'user': 'senser',
    'password': 'h@',
    'host': 'localhost',
    'database': 'weatherstation',
    'raise_on_warnings': True,
}

# parse arguments
verbose = False
interval = 10  # second
threshold = 37  # C

try:
    opts, args = getopt.getopt(sys.argv[1:], "vt:T:")
except getopt.GetoptError as err:
    print(str(err))
    print('measure.py -v -t <interval>')
    print('-v: be verbose')
    print('-t <interval>: measure each <interval> seconds (default: 10s)')
    print('-T <threshold>: raise alarm above this value')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-v':
        verbose = True
    elif opt == '-t':
        interval = int(arg)
    elif opt == '-T':
        threshold = int(arg)

# instantiate a sense-hat object
sh = sense_hat.SenseHat()

# infinite loop
try:
    while True:
        # instantiate a database connection
        try:
            mariadb_connection = mariadb.connect(**dbconfig)
            if verbose:
                print("Database connected")

        except mariadb.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Error: {}".format(err))
            sys.exit(2)

        # create the database cursor for executing SQL queries
        cursor = mariadb_connection.cursor(buffered=True)

        # get the sensor_id for temperature sensor
        try:
            cursor.execute("SELECT id FROM sensor WHERE name=%s", [sensor_name])
        except mariadb.Error as err:
            print("Error: {}".format(err))
            sys.exit(2)

        sensor_id = cursor.fetchone()
        if sensor_id is None:
            print("Error: no sensor found with naam = %s" % sensor_name)
            sys.exit(2)

        if verbose:
            print("Reading data from sensor %s with id %s" % (sensor_name, sensor_id[0]))

        # read last measurement from database
        stmt = 'SELECT value FROM measurement WHERE sensor_id = %s ORDER BY id DESC LIMIT 1'

        # read last measurement from database
        try:
            cursor.execute(stmt, sensor_id)
        except mariadb.Error as err:
            print("Error: {}".format(err))

        else:
            # fetch the data
            row = cursor.fetchone()

            # close db connection
            cursor.close()
            mariadb_connection.close()

            # check with threshold
            print(row[0])
            print(threshold)
            if (row[0] > threshold):
                # red
                sh.clear(255, 0, 0)
            else:
                # green
                sh.clear(0, 255, 0)

            if verbose:
                print("Temperature %s checked against threshold %s" % (row[0], threshold))

            # wait a while
            time.sleep(interval)

except KeyboardInterrupt:
    sh.clear()
    pass

# done
