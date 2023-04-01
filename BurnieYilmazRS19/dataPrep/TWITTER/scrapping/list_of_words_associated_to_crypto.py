
import mysql.connector as mysql
import pandas as pd


# enter your server IP address/domain name
HOST = "82.66.69.111"  # or "domain.com"
PORT = "3307"
UNIX_SOCKET = "/run/mysqld/mysqld10.sock"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "dico_terms"
# this is the user you create
USER = "charles3"
# user password
PASSWORD = "cQ3/HYb7VJ"

# connect to MySQL server
db_connection = mysql.connect(host=HOST, port=PORT, database=DATABASE,
                              unix_socket=UNIX_SOCKET, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
# enter your code here!
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()



list_to_insert = list()
names = ('crypto', 'btc', 'finance')
print(names)
for i in range (len(names)):
    list_to_insert.append(names[i])
as_pd_df = pd.DataFrame(list_to_insert)


def insert_into_existind_db(list_of_values):

    list_of_values = pd.DataFrame(list_of_values)
    # Preparing SQL query to INSERT a record into the database.
    insert_stmt = ("INSERT INTO dico_terms (string_term) VALUES (%s)")
    try:
        #Executing the SQL command
        for i in range(0, len(list_of_values)):
            print(list_of_values[i:i+1])
            row_val = list_of_values[i:i+1].values.flatten().tolist()
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


   
def retrieve_dico_of_terms():

    list_of_terms = []
    query = ("SELECT string_term FROM dico_terms ")

    db_cursor.execute(query)

    for (string_term) in db_cursor:
        list_of_terms.append(string_term[0])

    db_cursor.close()
    return(list_of_terms)

# insert_into_existind_db(as_pd_df)
# test = retrieve_dico_of_terms()
