import db_handler

company_symbol = input("Enter the symbol.")
company_name = input("Enter the company name.")
invest = input("Enter your current invest if any.")

con = db_handler.create_connection("./stock_db.db")
db_handler.create_table(con, db_handler.create_companies_table)
con.commit()
db_handler.insert_company_data(con, company_symbol, company_name, invest)
con.commit()
db_handler.close_connection(con)