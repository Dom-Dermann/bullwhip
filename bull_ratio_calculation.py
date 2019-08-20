def calc_income_ratios(historical_is):
    for year_data in historical_is:
        date_of_statement = year_data['date']
        try:
            year_revenue = float(year_data['Revenue'])
            year_net_income = float(year_data['Net Income'])
        except:
            pass

        year_net_profit_margin = round(year_net_income / year_revenue, 2)

        print(f'Year {date_of_statement} net profit margin is: {year_net_profit_margin}')