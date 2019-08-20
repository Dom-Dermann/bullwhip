import bull_api_calls
import numpy as np
import pandas as pd

class company:
    company_symbol = ""
    historical_income_statements = []
    key_metrics = []

    # constructor
    def __init__(self, symbol):
        self.company_symbol = symbol
        self.historical_income_statements = bull_api_calls.get_income_statements(self.company_symbol)
        self.key_metrics = bull_api_calls.get_key_metrics(self.company_symbol)

    # method to calculate all ratios
    def calculate_ratios(self):
        if self.historical_income_statements is not None:
            # calculate individual margins as Pandas Series
            npm = calc_net_profit_margin(self.historical_income_statements)
            gm = get_gross_margin(self.historical_income_statements)

            # combine Pandas Series with ratios to one report in the form of a Pandas DataFrame
            ratio_summary = pd.DataFrame({'net profit margin' : npm, 'gross profit margin' : gm})
            print(ratio_summary)

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