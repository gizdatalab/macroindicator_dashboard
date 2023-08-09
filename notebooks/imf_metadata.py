#SOURCE: http://www.bd-econ.com/imfapi2.html

import requests 
import pandas as pd

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'DataStructure/PGCS'  # Method / 


# Identify the different dimensions that are used in the dataset (e.g., frquency, country codes, indicator codes) 

dimension_list = requests.get(f'{url}{key}').json()\
            ['Structure']['KeyFamilies']['KeyFamily']\
            ['Components']['Dimension']
for n, dimension in enumerate(dimension_list):
    print(dimension['@codelist'])

# Retrieve the codes for one dimension (here example for country codes)

key = f"CodeList/{dimension_list[1]['@codelist']}"
code_list = requests.get(f'{url}{key}').json()\
	    ['Structure']['CodeLists']['CodeList']['Code']
for code in code_list:
    print(f"{code['Description']['#text']}: {code['@value']}")

