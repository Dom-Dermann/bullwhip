import data_provider
import numpy as np
import pandas as pd
import sqlite3
import db_handler

class Company:
    company_symbol = ""
    data_base = "./stock_db.db"
    income_statement_df = pd.DataFrame
    # historical_income_statements = []
    # key_metrics = []

    # constructor
    def __init__(self, symbol):
        self.company_symbol = symbol
        # open connection to DB and retrieve all entries with company symbol
        con = db_handler.create_connection(self.data_base)
        self.income_statement_df = pd.read_sql_query(f"SELECT * FROM income_statements WHERE symbol='{self.company_symbol}'", con)
        db_handler.close_connection(con)
        # self.historical_income_statements = data_provider.get_income_statements_from_API(self.company_symbol)
        # self.key_metrics = data_provider.get_key_metrics_from_API(self.company_symbol)

    # method to calculate all ratios
    def calculate_ratios(self):
        if self.historical_income_statements is not None:
            # calculate individual margins as Pandas Series
            npm = calc_net_profit_margin(self.historical_income_statements)
            gm = get_gross_margin(self.historical_income_statements)

            # combine Pandas Series with ratios to one report in the form of a Pandas DataFrame
            ratio_summary = pd.DataFrame({'net profit margin' : npm, 'gross profit margin' : gm})
            print(ratio_summary)

    def calculate_gross_margin(self):
        #iterate over every entry - every year recorded
        gross_maring_series = pd.Series()
        for index, row in self.income_statement_df.iterrows():
            gross_margin = float(row['gross_profit'] / row['total_revenue'])
            year_margin = pd.Series(gross_margin, index=[row['year']])
            gross_maring_series = gross_maring_series.append(year_margin)
        return(gross_maring_series)

    def calculate_profit_maring(self):
        #iterate over every entry - every year recorded
        profit_maring_series = pd.Series()
        for index, row in self.income_statement_df.iterrows():
            profit_margin = float(row['net_income_applicable_to_common_shares'] / row['total_revenue'])
            year_margin = pd.Series(profit_margin, index=[row['year']])
            profit_maring_series = profit_maring_series.append(year_margin)
        return(profit_maring_series)


    ### financial modelling prep API stuff
    ###
    ###

    def get_screening_indicators(self):
        try:
            price_book = float(self.key_metrics[0]['PB ratio'])
            price_earnings = float(self.key_metrics[0]['PE ratio'])
        except:
            pass

        if price_book > 1.5:
            print(f'Failed screening according to Graham / Buffet. P/B is {price_book} and should be <1.5.')
        if price_earnings > 15:
            print(f'Failed screening according to Graham / Buffet. P/E is {price_earnings} and should be <15')
        else:
            print("Passed screening according to Graham / Buffet.")


def calc_net_profit_margin(historical_is):
    hist_prof_margins = pd.Series()

    for year_data in historical_is:
        date_of_statement = year_data['date']
        try:
            year_revenue = float(year_data['Revenue'])
            year_net_income = float(year_data['Net Income'])
        except:
            pass

        year_net_profit_margin = round(year_net_income / year_revenue, 2)
        hist_prof_margins[date_of_statement] = year_net_profit_margin
    
    return hist_prof_margins

def get_gross_margin(historical_is):
    hist_gross_margin = pd.Series()

    for year_data in historical_is:
        date_of_statement = year_data['date']
        try:
            year_gross_margin = float(year_data['Gross Margin'])
        except:
            pass
        
        hist_gross_margin[date_of_statement] = year_gross_margin
    
    return hist_gross_margin