from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import urllib


# This scrapes the yahoo finance page
# ATTENTION - this may need updating as the yahoo finance website layout changes
# results are then saved to local sqlite3 database
def get_balance_sheet(symbol):
    URL = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol
    page = requests.get(URL)
    

    return df

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