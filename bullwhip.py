from bull_ratio_calculation import Company
import data_provider
import argparse
import db_handler

if __name__ == "__main__":
    """
    Usage: ./bullwhip COM
    """
    parser = argparse.ArgumentParser(description="Give the machine a company symbol to work with.")
    parser.add_argument('company_symbol', nargs=1)
    parser.add_argument("--scrape", help="set this flag if you want to scrape for new data", action="store_true")
    args = parser.parse_args()
    c_symbol = args.company_symbol[0]

    # please specifiy when you wish to scrape again - no need to scrape the website every time, 
    # since statements are only release quarterly
    if args.scrape == True:
        data_provider.get_income_statement(c_symbol)

    company = Company(c_symbol)
    # gross_margin = company.calculate_gross_margin()
    # profit_margin = company.calculate_profit_margin()
    # operating_margin = company.calculate_operating_margin()
    # print("Gross margin \n" + str(gross_margin))
    # print("Operating margin \n" + str(operating_margin))
    # print("Profit margin \n" + str(profit_margin))
    data_provider.get_key_statistics(c_symbol)