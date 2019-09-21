import bull_ratio_calculation
import data_provider
import argparse

if __name__ == "__main__":
    """
    Usage: ./bullwhip COM
    """
    parser = argparse.ArgumentParser(description="Give the machine a company symbol to work with.")
    parser.add_argument('company_symbol', nargs=1)
    args = parser.parse_args()
    c_symbol = args.company_symbol[0]

    # uncomment when development of scarper is done
    # company = bull_ratio_calculation.company(c_symbol)
    # company.calculate_ratios()
    # company.get_screening_indicators()

    bs = data_provider.get_income_statement(c_symbol)
    print(bs)