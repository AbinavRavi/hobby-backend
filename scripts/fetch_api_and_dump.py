import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import json

load_dotenv()
# Replace these with your own database connection details
database_name = os.getenv("MASTER_DB_NAME")
user = os.getenv("MASTER_DB_USER")
password = os.getenv("MASTER_DB_PASSWORD")
host = os.getenv("MASTER_DB_HOST")
port = os.getenv("MASTER_DB_PORT") 

# def create_database():
#         try:
#             conn = psycopg2.connect(
#                 host=host,
#                 port=port,
#                 user=user,
#                 password=password,
#             )
#             conn.autocommit = True
#             cursor = conn.cursor()
#             cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
#             print(f"Database '{database_name}' created")
#             cursor.close()
#             conn.close()
#         except Exception as e:
#             print("Error:", e)

# create_database()

# Specify the path to your SQL file
sql_file_path = 'sql/insert_master.sql'
connection = None

try:
    connection = psycopg2.connect(
        database=database_name,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = connection.cursor()

    # cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), [database_name])
    # exists = cursor.fetchone()

    # if not exists:
    #     # Create the new database
    #     cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(database_name)))
    #     print(f"Database '{database_name}' created successfully.")

    # else:
    #     print(f"Database '{database_name}' already exists.")
    print("Successfully connected to the database")

    #get the data
    with open("/Users/abinavr/Desktop/namora/api_us_1.json") as file:
        data = json.load(file)

    # Read the SQL script from the file
    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    for item in data["rows"]:
        cursor.execute(sql_script, item)
        connection.commit()

    # Execute the SQL script
    # cursor.execute(sql_script)
    # connection.commit()
    print("SQL script executed successfully")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed")
