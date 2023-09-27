import mysql.connector as mysql

HOST = "mysql"
DATABASE = "test"
USER = "root"
PASSWORD = "root"

db_connection = mysql.connect(host=HOST, 
                              database=DATABASE, 
                              user=USER, 
                              password=PASSWORD)

print("Connected to:", db_connection.get_server_info())
print(db_connection.database)