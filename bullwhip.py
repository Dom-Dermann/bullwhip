import bull_api_calls
import bull_ratio_calculation
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Give the machine a company symbol to work with.")
    parser.add_argument('company_symbol', nargs=1)
    args = parser.parse_args()
    c_symbol = args.company_symbol[0]

    historical_is = bull_api_calls.get_stock_info(c_symbol)
    if historical_is is not None:
        bull_ratio_calculation.calc_income_ratios(historical_is)