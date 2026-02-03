import mysql.connector
print("MySQL Connector imported successfully.")
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
print("Connection to MySQL database established.")
con.close()