import requests
import json

def get_stock_info(company_short):
    api_url_income_statement = f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company_short}'

    response = requests.get(api_url_income_statement)
    income_statement_data = json.loads(response.text)

    historical_is = income_statement_data['financials']
    print(f'Historical data found for the last {len(historical_is)} years.')
    return historical_is