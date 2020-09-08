import sys, getopt
import argparse
import sense_hat
import time
import os
import mysql.connector as mariadb
from mysql.connector import errorcode

dbconfig = {
    'user': 'sensem',
    'password': 'h@',
    'host': 'localhost',
    'database': 'weatherstation',
    'raise_on_warnings': True,
}

measurement_count = 0
sh = sense_hat.SenseHat()

def countdown(t):
    global verbose
    
    if verbose:
        print("Restarting the program after %s seconds" % t)
    
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        
        if verbose:
            print(timeformat, end='\r')
        
        time.sleep(1)
        t -= 1
    
    if verbose:    
        print('Restarting the program...\n\n\n\n\n')

# Create an infinite loop for getting the temperature every 10 seconds.
try:
    while True:
        sensor_name = 'Luchtdruk'
        verbose = True
        interval = 20 # Seconds
        try:
            opts, args = getopt.getopt(sys.argv[1:], "vt:S:")
        except getopt.GetoptError as error:
            print("Something went wrong")
            print(str(error))
            print('measure.py -S -q -t <interval>')
            print('-S: sensor name')
            print('-q: be quiet')
            print('-t <interval>: measure each <interval> seconds (default: 10s)')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-q':
                verbose = False
            elif opt == '-t':
                interval = int(arg)
            elif opt == '-S':
                sensor_name = arg
        
        measurement_count += 1
        if verbose:
            print("Measurement: %s" % measurement_count)

        try:
            database_connection = mariadb.connect(**dbconfig)
            if verbose:
                print("Database connected")
        except mariadb.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your username or password")
                sys.exit(2)
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                sys.exit(2)
        
            print("Error: {}".format(error))
            sys.exit(2)
    
        cursor = database_connection.cursor()
        #cursor.autocommit = True # Turn autocommit on or of.
    
        # Determine the sensor id for the temperature sensor.
        try:
            cursor.execute("SELECT * FROM sensor WHERE name=%s;", [sensor_name])
        except mariadb.Error as error:
            print("Error: {}".format(error))
            sys.exit(2)

        sensor_data = cursor.fetchone()
        if sensor_data == None:
            print("Erorr: no sensor found with name = %s" % sensor_name)
            sys.exit(2)
        if verbose:
            print("Reading data from sensor %s with id %s" % (sensor_data[1], sensor_data[0]))
        
        
        airpressure = round(sh.get_pressure(), 2)
        
        if verbose:
            print("%s: %s %s" % (sensor_data[1], airpressure, sensor_data[2]))
        
        # Save the readed data from the sensor in the database.
        try:
            cursor.execute("INSERT INTO measurement (value, sensor_id) VALUES (%s, %s);", [airpressure, sensor_data[0]])
        except mariadb.Error as error:
            print("Error: {}".format(error))
            sys.exit(2)
            
        database_connection.commit()
        if verbose:
            print("Sensor data committed")
        
        cursor.close()
        database_connection.close()
        
        # Wait a while before re-reading the data from the sensor.    
        countdown(interval)
        
except KeyboardInterrupt:
    print("Stop reading the data from the sensor.")
    
    cursor.close()
    database_connection.close()
    sys.exit(2)
except:
    print("Something went wrong")
    sys.exit(2)
    
