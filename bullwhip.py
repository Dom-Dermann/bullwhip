import bull_ratio_calculation
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Give the machine a company symbol to work with.")
    parser.add_argument('company_symbol', nargs=1)
    args = parser.parse_args()
    c_symbol = args.company_symbol[0]

    company = bull_ratio_calculation.company(c_symbol)
    company.calculate_ratios()