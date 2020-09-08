#!/usr/bin/python3

# import connection module; name it mariadb
import mysql.connector as mariadb

# connect to the database
mariadb_connection = mariadb.connect(
    user='senser',
    password='h@',
    database='weerstation')

# create a cursor object for executing queries
cursor = mariadb_connection.cursor()

# prepare a select query
stmt = "SELECT tijd, UNIX_TIMESTAMP(tijd) as t, waarde FROM meting"

# execute the query (parameter must be a tuple)
cursor.execute(stmt)

# print returned rows
print("Content-type: text/plain\n")
row = cursor.fetchone()
while row is not None:
    print("tijd: %s (%s), waarde: %s" % (row[0], row[1], row[2]))
    row = cursor.fetchone()

# close cursor and database
cursor.close()
mariadb_connection.close()

# done
print("Einde script")
