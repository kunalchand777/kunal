# mysql_crud.py
import mysql.connector
try:
    conn=mysqldb.connector.connect(
        host="localhost",
        user="kunalchand",
        password="1008"
        database="gaming"
    )
    ifconn.is_connected():
    print("Successfully connected to the database")
except mysqldb.connector.Error as e:
    print("Error while connecting to MySQL", e)
finally:    
    if conn.is_connected():
        conn.close()
        print("MySQL connection is closed")