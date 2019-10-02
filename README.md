# bullwhip
A financial analysis tool - deprecated

Yahoo finance scraping no longer works due to a re-design of their website, see bullwhip 2.0 for current version. This supports less company symbols but is build on a reliable API infrastructure. 

Please note: if you wish to use this program be aware that it scrapes some websites. 
While this does not violate the terms of use, please make sure you do not interfere with their business by being conscious 
of how many requests you send. 
Thank you. 

How to use:
always activate the virtual environment first (./bullwhip/Scripts/activate)
Provide the bullwhip.py script with a company symbol (i.e. python bullwhip.py AAPL)
You can feed the database with your own list of companies that can then be crawled automatically. python bull_add_company.py AAPL
