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
            npm = calc_net_profit_margin(self.historical_income_statements)
            print(npm)





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