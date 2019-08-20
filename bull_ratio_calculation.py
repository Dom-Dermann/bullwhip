import bull_api_calls
import numpy as np
import pandas as pd

class company:
    company_symbol = ""
    historical_income_statements = []

    # constructor
    def __init__(self, symbol):
        self.company_symbol = symbol
        self.historical_income_statements = bull_api_calls.get_income_statements(self.company_symbol)

    # method to calculate all ratios
    def calculate_ratios(self):
        if self.historical_income_statements is not None:
            # calculate individual margins as Pandas Series
            npm = calc_net_profit_margin(self.historical_income_statements)
            gm = get_gross_margin(self.historical_income_statements)

            # combine Pandas Series with ratios to one report in the form of a Pandas DataFrame
            ratio_summary = pd.DataFrame({'net profit margin' : npm, 'gross profit margin' : gm})
            print(ratio_summary)


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