import sqlite3
from sqlite3 import Error

### creation statements

create_companies_table = """CREATE TABLE IF NOT EXISTS companies (
    symbol text PRIMARY KEY,
    name text NOT NULL,
    invest integer,
    UNIQUE (symbol)
); """

create_yahoo_ratios_table = """ CREATE TABLE IF NOT EXISTS yahoo_ratios (
    ratio_id integer PRIMARY KEY,
    symbol text,
    year date,
    market_cap integer, 
    enterprise_value integer,
    trailing_pe integer,
    forward_pe integer,
    peg_ratio integer,
    price_sales integer,
    price_book integer,
    enterprise_value_revenue integer,
    enterprise_value_EBITDA integer,
    beta integer,
    year_change integer,
    SandP500_52_week_change integer,
    year_high integer, 
    year_low integer,
    fifty_day_moving_avg integer,
    twohundred_day_moving_avg integer,
    three_month_vol_avg integer,
    ten_day_vol_avg integer,
    shares_outstanding integer,
    float integer,
    percent_held_by_insiders integer,
    percent_held_by_institutions integer,
    shares_short integer, 
    short_ratio integer,
    short_percent_of_float integer,
    short_percent_of_shares_outstanding integer,
    share_short_perivous_month integer,
    forward_anual_dividend_rate integer,
    forward_anual_dividend_yield integer,
    trailing_anual_dividend_rate integer,
    trailing_anual_dividend_yield integer,
    five_year_average_dividend_yield integer,
    payout_ratio integer,
    dividend_date date,
    ex_dividend_date date,
    last_split_factor integer,
    last_split_date integer,
    fiscal_year_end date,
    most_recent_quarter date,
    return_on_assets integer,
    return_on_equity integer,
    revenue integer,
    revenue_per_share integer,
    quarterly_revenu_growth integer,
    gross_proft integer,
    EBITDA integer,
    net_income_avi_to_common integer,
    diluted_eps integer,
    quarterly_earnings_growth integer,
    total_cash integer,
    total_cash_per_share integer,
    total_debt integer,
    total_debt_equity integer,
    current_ratio integer,
    book_value_per_share integer,
    operating_cash_flow integer,
    levered_free_cash_flow integer,
    FOREIGN KEY (symbol) REFERENCES companies (symbol),
    UNIQUE(symbol, year)
); """

create_income_statements_table = """ CREATE TABLE IF NOT EXISTS income_statements (
    id integer PRIMARY KEY, 
    symbol text,
    year date, 
    total_revenue integer, 
    cost_of_revenue integer,
    gross_profit integer, 
    research_development integer, 
    selling_general_and_administrativ integer, 
    non_recurring integer, 
    others integer, 
    total_operating_expenses integer, 
    operating_income integer, 
    total_other_income integer, 
    EBITA integer, 
    interest_expense integer, 
    IBT integer, 
    income_tax_expense integer, 
    minority_interest integer, 
    net_income_from_continuing_ops integer, 
    discontinued_operations integer, 
    extraordinary_items integer,
    effect_of_accounting_changes integer,
    other_items integer,
    preferred_stock integer,
    net_income_applicable_to_common_shares integer,
    FOREIGN KEY (symbol) REFERENCES companies (symbol),
    UNIQUE(symbol, year)
);"""

### DB methods

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

def close_connection(conn):
    conn.close()
    return True

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_company_data(conn, symbol, name, invest):
    sql = "INSERT OR IGNORE INTO companies VALUES (?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, [symbol, name, invest])
    conn.commit

def insert_income_statement_data(conn, income_statement):
    sql = """ INSERT INTO income_statements (
    symbol,
    year, 
    total_revenue, 
    cost_of_revenue,
    gross_profit, 
    research_development, 
    selling_general_and_administrativ, 
    non_recurring, 
    others, 
    total_operating_expenses, 
    operating_income, 
    total_other_income, 
    EBITA, 
    interest_expense, 
    IBT, 
    income_tax_expense, 
    minority_interest, 
    net_income_from_continuing_ops, 
    discontinued_operations, 
    extraordinary_items,
    effect_of_accounting_changes,
    other_items,
    preferred_stock,
    net_income_applicable_to_common_shares
    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, income_statement)
    conn.commit()
    return cur.lastrowid


### for testing only
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