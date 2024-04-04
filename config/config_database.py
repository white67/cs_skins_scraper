import mysql.connector
from mysql.connector import Error
from datetime import datetime

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "mansionmusik1400"
DB_DATABASE = "skins_valued"

BUFFIDS = "buffids"
BUFFIDS_ITEM_NAME = "item_name"
BUFFIDS_BUFF_ID = "buff_id"


# connect with database
def db_connect():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWD,
        database=DB_DATABASE
    )
    # set buffer
    cursor = db.cursor(buffered=True)
    return db, cursor


# close connection
def db_close(db, cursor):
    cursor.close()
    db.close()


# add to database
def db_add(db, cursor, table_name, columns, data):
    try:
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"""INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"""
        cursor.execute(query, data)
        db.commit() 
        print(f"[{table_name}] Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs


# function to check if entry in database (in single table) already exists
def check_duplicate(cursor, table_name, columns, data):
    # Construct the WHERE clause dynamically based on the columns provided
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    cursor.execute(query, data)
    result = cursor.fetchone()
    # Check if any row was fetched (meaning there's already a duplicate entry)
    return False if result == None else True


def db_update(db, cursor, table_name, columns, data, columns_to_check, data_to_check):
    try:
        if len(data_to_check) == 0:
            where_clause = ''
            existance = True
            updated_data = data
        else:
            where_clause = " AND ".join(f"{column} = %s" for column in columns_to_check)
            where_clause = f" WHERE {where_clause}"
            existance = check_duplicate(cursor, table_name, columns_to_check, data_to_check)
            updated_data = data + data_to_check
            
        if existance:
            updated_str = ', '.join(f"{column} = %s" for column in columns)
            update_query = (f"UPDATE {table_name} SET {updated_str}{where_clause};")
            cursor.execute(update_query, updated_data)
            db.commit()
            print(f"[{table_name}] Entry updated successfully.")
            print(f"{data}")
        else:
            print(f"[{table_name}] Entry does not exist: {data_to_check}")
            # db_add(db, cursor, PLAYERS, [PLAYERS_PLAYER_NAME, PLAYERS_SOFASCORE_LINK, PLAYERS_TEAM, PLAYERS_BIRTH_DATE], [player_name, sofascore_link, team_name, birth_date])
            
            # try adding again
            # here add code but it seems like it needs to be class object
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs


def get_id(cursor, id_data, table_name, columns, data):
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    
    # Construct the SELECT query
    query = f"SELECT {id_data} FROM {table_name} WHERE {where_clause}"
    
    cursor.execute(query, data)
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        return None