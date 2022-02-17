import mysql.connector as mysql
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import sqlalchemy as sq
from .get_data_api_b import get_pd_histo
import mplfinance as mpf



# enter your server IP address/domain name
HOST = "82.66.69.111"  # or "domain.com"
PORT = "3307"
UNIX_SOCKET = "/run/mysqld/mysqld10.sock"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "Crypto"
# this is the user you create
USER = "charles2"
# user password
PASSWORD = "cH9)J8i3lp"
print("good here")

# connect to MySQL server
db_connection = mysql.connect(host=HOST, port=PORT, database=DATABASE,
                              unix_socket=UNIX_SOCKET, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
# enter your code here!
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()
# get list of all databases
db_cursor.execute("SHOW DATABASES")
# print all databases
for db in db_cursor:
    print(db)





# Preparing SQL query to INSERT a record into the database.
insert_stmt = (
   "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)"
   "VALUES (%s, %s, %s, %s, %s)"
)

try:
   # Executing the SQL command
   db_cursor.execute(insert_stmt, data)
   
   # Commit your changes in the database
   db_connection.commit()

except:
   # Rolling back in case of error
   db_connection.rollback()

print("Data inserted")

