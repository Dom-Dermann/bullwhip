from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib
import json
import db_handler
import datetime

# path to local database
database = "./stock_db.db"

# This scrapes the yahoo finance page
# ATTENTION - this may need updating as the yahoo finance website layout changes
# results are then saved to local sqlite3 database
def get_income_statement(symbol):
    URL = f'https://finance.yahoo.com/quote/{symbol}/financials?p={symbol}'

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
            print('changes committed to income statements table ...')
            # close connection
            db_handler.close_connection(conn)
        
def get_key_statistics(symbol):
    URL = f'https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}'

    response = requests.get(URL)
    # check if website was reachable
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'lxml')
        table = str(soup.findAll('table'))
        # check if webseite contains a table
        if table: 
            converted_table = pd.read_html(table)
            # get valuation measures
            valuation_measures_df = pd.DataFrame(converted_table[0])
            # get stock price history
            financial_highlights_df = pd.DataFrame(converted_table[1])
            # get share statistics
            share_statistics_df = pd.DataFrame(converted_table[2])
            # get dividends and splits
            dividends_df = pd.DataFrame(converted_table[3])
            # get fiscal year
            fiscal_year_df = pd.DataFrame(converted_table[4])
            # get profitability ratios
            profitability_df = pd.DataFrame(converted_table[5])
            # get management effectiveness ratios
            management_df = pd.DataFrame(converted_table[6])
            # get income statement ratios
            is_ratio_df = pd.DataFrame(converted_table[7])
            # get balance sheet ratios
            bs_ratios_df = pd.DataFrame(converted_table[8])
            # get cash flow statement ratios
            cf_ratios_df = pd.DataFrame(converted_table[9])
            # create one data frame from all tables
            df_key_ratios = valuation_measures_df.append([financial_highlights_df, share_statistics_df, dividends_df, fiscal_year_df, profitability_df, management_df, is_ratio_df, bs_ratios_df, cf_ratios_df])
            # prepare df for insertion
            df_key_ratios = df_key_ratios.swapaxes('index', 'columns')
            df_key_ratios.columns = df_key_ratios.iloc[0]
            df_key_ratios = df_key_ratios.drop([0])
            print(df_key_ratios)
        
            #create yahoo_ratios table if not exists
            conn = db_handler.create_connection("./stock_db.db")
            if conn is not None:
                db_handler.create_table(conn, db_handler.create_yahoo_ratios_table)
                conn.commit()
                print("Creating key ratios table ...")
            else:
                print('Error, DB connection not established.')

            #commit data ratio data to DB
            one_year = df_key_ratios.index[0].tolist()
            print(one_year)
            # date = datetime.datetime.today().strftime("%Y-%m-%d")
            # one_year.insert(0, date)
            # one_year.insert(0, symbol)
            # db_handler.insert_key_ratio_data(conn, one_year)

            #close connection
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