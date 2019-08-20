import requests
import json

def get_income_statements(company_short):
    api_url_income_statement = f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company_short}'

    response = requests.get(api_url_income_statement)
    if response.status_code == 200:
        income_statement_data = json.loads(response.text)
        try:
            historical_is = income_statement_data['financials']
            print(f'Historical income statement data found for the last {len(historical_is)} years.')
            return historical_is
        except:
            print("There are no records for the company under the symbol you provided.")
    else:
        raise Exception("Could not retrieve company data from API.")

def get_key_metrics(company_short):
    api_url_metrics = f'https://financialmodelingprep.com/api/v3/company-key-metrics/{company_short}'

    response = requests.get(api_url_metrics)
    if response.status_code == 200:
        metrics_data = json.loads(response.text)
        try:
            historical_is = metrics_data['metrics']
            print(f'Metrics data found for the last {len(historical_is)} years.')
            return historical_is
        except:
            print("There are no records for the company under the symbol you provided.")
    else:
        raise Exception("Could not retrieve company data from API.")
