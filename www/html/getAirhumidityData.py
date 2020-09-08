#!/usr/bin/python

# import connection module; name it mariadb
import mysql.connector as mariadb
import json

# initialize
data = []

# connect to the database
mariadb_connection = mariadb.connect(
    user='senser',
    password='h@',
    database='weatherstation')

# create a cursor object for executing queries
cursor = mariadb_connection.cursor()

# prepare a select query (last 100 items)
stmt = "SELECT UNIX_TIMESTAMP(time) as unixtime, value FROM measurement WHERE sensor_id = 2 ORDER BY unixtime DESC LIMIT 100"

# execute the query (parameter must be a tuple)
cursor.execute(stmt)

num_fields = len(cursor.description)
field_names = [i[0] for i in cursor.description]

# returned rows (tuples)
rows = cursor.fetchall()

# sort the array, ascending
rows.sort(key=lambda x:x[0])

# close cursor and database
cursor.close()
mariadb_connection.close()

output_json = []
for row in rows:
    output_json.append(dict(zip(field_names, row)))

print("Content-type: application/json\n")
print(json.dumps(output_json))
# done
