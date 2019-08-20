import bull_api_calls
import bull_ratio_calculation

historical_is = bull_api_calls.get_stock_info("AAPL")
bull_ratio_calculation.calc_income_ratios(historical_is)