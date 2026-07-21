"""Apply database schema to a Postgres database using SUPABASE_DB_* env vars.

Usage:
  Set the following environment variables (Streamlit secrets or local env):
    SUPABASE_DB_HOST, SUPABASE_DB_NAME, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD, SUPABASE_DB_PORT
  Then run:
    python scripts/apply_schema.py

This script executes database/01_create_schema.sql against the target DB.
"""
import os
import sys

try:
    import psycopg2
except Exception as e:
    print("psycopg2 is required. Install with: pip install psycopg2-binary")
    raise

SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', '01_create_schema.sql')

HOST = os.getenv('SUPABASE_DB_HOST')
NAME = os.getenv('SUPABASE_DB_NAME')
USER = os.getenv('SUPABASE_DB_USER')
PASSWORD = os.getenv('SUPABASE_DB_PASSWORD')
PORT = int(os.getenv('SUPABASE_DB_PORT', '5432'))

if not (HOST and NAME and USER and PASSWORD):
    print('Missing SUPABASE_DB_* environment variables. Aborting.')
    sys.exit(1)

with open(SQL_PATH, 'r', encoding='utf8') as f:
    sql = f.read()

print(f'Connecting to {HOST}:{PORT}/{NAME} as {USER}...')
conn = psycopg2.connect(host=HOST, dbname=NAME, user=USER, password=PASSWORD, port=PORT, sslmode='require')
conn.autocommit = True
cur = conn.cursor()
try:
    print('Executing schema...')
    cur.execute(sql)
    print('Schema applied successfully.')
except Exception as e:
    print('Error applying schema:', e)
    raise
finally:
    cur.close()
    conn.close()
