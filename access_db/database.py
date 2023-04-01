import mysql.connector as mysql
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import sqlalchemy as sq
from get_data_api_b import get_pd_daily_histo
import mplfinance as mpf
import MySQLdb as mysql2

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

# connect to MySQL server
db_connection = mysql.connect(host=HOST, port=PORT, database=DATABASE,
                              unix_socket=UNIX_SOCKET, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
# enter your code here!
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()



def insert_into_existind_db(symbol_name, start_date):

   hist_df = get_pd_daily_histo(symbol_name, start_date)
   list_name_col = hist_df.columns
   size_df = hist_df.size

   hist_df['Open_Time'] = hist_df['Open_Time'].astype(str)
   hist_df['Close_Time'] = hist_df['Close_Time'].astype(str)

   statement_1 = "INSERT INTO " + symbol_name

   # Preparing SQL query to INSERT a record into the database.
   insert_stmt = (
       statement_1 + " (Open_Time, Open, High, Low, Close, Volume, Close_Time, Number_of_Trades) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
   )

   try:
      #Executing the SQL command
      for i in range(0, size_df-1):
         row_val = hist_df[i:i+1].values.flatten().tolist()
         db_cursor.execute(insert_stmt, row_val)
         db_connection.commit()
      # Commit your changes in the database
      
      print("Data inserted")

   except TypeError as e:
      print("Data could not be inserted")
      # Rolling back in case of error
      print(e)
      db_connection.rollback()
   return(0)

def create_db(symbol_name):

   statement_start = "DROP TABLE IF EXISTS " + symbol_name
   #Dropping BTCUSDT table if already exists.
   db_cursor.execute(statement_start)

   statement_end = "CREATE TABLE " + symbol_name
   #Creating table as per requirement
   sql = statement_end + ''' (
      id int NOT NULL AUTO_INCREMENT,
      Open_Time datetime NOT NULL,
      Open  decimal(19,4) NULL,
      High  decimal(19,4) NULL,
      Low  decimal(19,4) NULL,
      Close  decimal(19,4) NULL,
      Volume bigint NULL, 
      Close_Time datetime NOT NULL, 
      Number_of_Trades bigint NULL,
      PRIMARY KEY (id)
   )AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
   '''
   db_cursor.execute(sql)

   return(0)

   
