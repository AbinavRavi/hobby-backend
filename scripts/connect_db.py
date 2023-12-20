import psycopg2
from psycopg2 import sql

db_params = {
    "database": "postgres",
    "user": "namora",
    "password": "namoraadmin",
    "host": "master-db.c3rrmcm1vc6s.us-west-2.rds.amazonaws.com",
    "port": "5432",
}
try:
    print("before connection")
    conn = psycopg2.connect(**db_params)
    print(conn)
    cursor = conn.cursor()
    # Use the "information_schema" to check if the database exists
    query = sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;")
    cursor.execute(query, [db_params["database"]])

    # Fetch the result
    result = cursor.fetchone()
    if result[0] == 1:
        print(True)
except Exception as e:
    print(e)