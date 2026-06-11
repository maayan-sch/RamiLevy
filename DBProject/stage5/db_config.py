import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "ramiLevy",
    "user": "MaayanRavid",
    "password": "MaayanRavid",  
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)