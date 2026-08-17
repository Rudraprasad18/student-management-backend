import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

with connection.cursor() as cursor:
    cursor.execute("SELECT current_user, current_database();")
    result = cursor.fetchone()

print("Connected successfully!")
print("User:", result[0])
print("Database:", result[1])

connection.close()