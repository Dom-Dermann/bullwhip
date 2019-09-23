from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib
import json
import db_handler

# path to local database
database = "./stock_db.db"

# This scrapes the yahoo finance page
# ATTENTION - this may need updating as the yahoo finance website layout changes
# results are then saved to local sqlite3 database
def get_income_statement(symbol):
    URL = f'https://finance.yahoo.com/quote/{symbol}/financials?p=DAI.DE'

    response = requests.get(URL)
    # check if website was reachable
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'lxml')
        table = str(soup.find('table'))
        # check if webseite contains a table
        if table: 
            df = pd.DataFrame(pd.read_html(table)[0])
            # convert index and columns
            df.columns = df.iloc[0]
            df = df.drop([0])
            df = df.set_index('Revenue')

            #clean up the data
            df = df.drop(['Operating Expenses', 'Income from Continuing Operations', 'Non-recurring Events', 'Net Income'])
            
            # create connection to DB
            conn = db_handler.create_connection(database)

            # create income statements tables if not there yet
            if conn is not None:
                db_handler.create_table(conn, db_handler.create_income_statements_table)
                conn.commit()
                print("Creating income statement table ...")
            else:
                print('Error, DB connection not established.')

            # save income statement data to table
            # list of data for one year:
            df = df.swapaxes('index', 'columns')
            # iterate over all years present
            for index, row in df.iterrows():
                one_year = row.tolist()
                # get date from dataframe header and add
                date = index
                one_year.insert(0, date)
                # add company symbol
                one_year.insert(0, symbol)
                db_handler.insert_income_statement_data(conn, one_year)
            # close connection
            db_handler.close_connection(conn)
        

# implements API calls as backup (only works for US traded stocks)
def get_income_statements_from_API(company_short):
    api_url_income_statement = f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company_short}'

    response = requests.get(api_url_income_statement)
    if response.status_code == 200:
        income_statement_data = json.loads(response.text)
        try:
            historical_is = income_statement_data['financials']
            print(f'Historical income statement data found for the last {len(historical_is)} years.')
            return historical_is
        except:
            raise Exception("There are no records for the company under the symbol you provided.")
    else:
        raise Exception("Could not retrieve company data from API.")

def get_key_metrics_from_API(company_short):
    api_url_metrics = f'https://financialmodelingprep.com/api/v3/company-key-metrics/{company_short}'

    response = requests.get(api_url_metrics)
    if response.status_code == 200:
        metrics_data = json.loads(response.text)
        try:
            historical_is = metrics_data['metrics']
            print(f'Metrics data found for the last {len(historical_is)} years.')
            return historical_is
        except:
            raise Exception("There are no records for the company under the symbol you provided.")
    else:
        raise Exception("Could not retrieve company data from API.")