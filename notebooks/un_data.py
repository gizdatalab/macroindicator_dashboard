#DOCUMENTATION: https://population.un.org/dataportal/about/dataapi
#LIST OF INDICATORS: https://population.un.org/dataportalapi/api/v1/indicators

import pandas as pd
import requests
import json

# define base url 

BASE_URL = "https://population.un.org/dataportalapi/api/v1/locations"


# Creates the target URL, indicators, in this instance
target = BASE_URL + "/locations"

# Get the response, which includes the first page of data as well as information on pagination and number of records
response = requests.get(BASE_URL)
print(response)

# # Converts call into JSON
# j = response.json()


# # Converts JSON into a pandas DataFrame.
# df = pd.json_normalize(j['data']) # pd.json_normalize flattens the JSON to accomodate nested lists within the JSON structure

# # Loop until there are new pages with data
# while j['nextPage'] != None:
#     # Reset the target to the next page
#     target = j['nextPage']

#     #call the API for the next page
#     response = requests.get(target)

#     # Convert response to JSON format
#     j = response.json()

#     # Store the next page in a data frame
#     df_temp = pd.json_normalize(j['data'])

#     # Append next page to the data frame
#     df = df.append(df_temp)

# print(df)

# # identify the max ID for the countries to be queried
# # Source: https://population.un.org/dataportalapi/api/v1/locations?pageNumber=1

# #response = requests.get("https://population.un.org/dataportalapi/api/v1/locations?pageNumber=1")
# #j=response.json()
# #print(j)

# # Creates the target URL, indicators, in this instance
# #target = BASE_URL + "/data/indicators/49/locations/4/start/2005/end/2010"
# #target = BASE_URL + "/locations"

# # Get the response, which includes the first page of data as well as information on pagination and number of records
# #response = requests.get(target)

# # Converts call into JSON
# #j = response.json()

# #print(j)

# # Extracting the "id" values
# #id_list = [item['id'] for item in j]
# #print(id_list)

# # Converts JSON into a pandas DataFrame.
# #df = pd.json_normalize(j['data']) # pd.json_normalize flattens the JSON to accomodate nested lists within the JSON structure

# #print(df)
# # # Loop until there are new pages with data
# # while j['nextPage'] != None:
# #     # Reset the target to the next page
# #     target = j['nextPage']

# #     #call the API for the next page
# #     response = requests.get(target)

# #     # Convert response to JSON format
# #     j = response.json()

# #     # Store the next page in a data frame
# #     df_temp = pd.json_normalize(j['data'])

# #     # Append next page to the data frame
# #     df = df.append(df_temp)