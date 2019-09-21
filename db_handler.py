import sqlite3
from sqlite3 import Error

### creation statements

create_companies_table = """CREATE TABLE IF NOT EXISTS companies (
    symbol text PRIMARY KEY,
    name text NOT NULL,
    invest integer
); """

create_income_statements_table = """ CREATE TABLE IF NOT EXISTS income_statements (
    id integer PRIMARY KEY, 
    symbol text,
    year date, 
    total_revenue integer, 
    cost_of_revenue integer,
    FOREIGN KEY (symbol) REFERENCES companies (symbol)
);"""

def create_connection(db_file):
    # create connection to sqlite db
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('connected to DB version: ' + sqlite3.version)
        return conn
    except Error as e: 
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "./stock_db.db"
    
    # create connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, create_companies_table)
        create_table(conn, create_income_statements_table)
        conn.commit()
    else:
        print('Error, DB connection not established.')

if __name__ == "__main__":
    main()