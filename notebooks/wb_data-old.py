import requests
import pandas as pd
import numpy as np

#SOURCE:https://github.com/shwetajoshi601/world-bank-data-analysis/blob/master/world-bank-data-eda.ipynb


# List of indicators according to the features defined above
INDICATOR_CODES=['NY.GDP.PCAP.PP.CD', 
                 'NY.GDP.MKTP.KD.ZG'] 
                 #'SL.EMP.SELF.ZS',
                 #'EG.FEC.RNEW.ZS',
                 #'NE.TRD.GNFS.ZS',
                 #'BX.KLT.DINV.WD.GD.ZS'
                 #'SL.EMP.VULN.FE.ZS']

COUNTRY_LIST=['USA',
              'India', 
              'China'
              ]

START_YEAR = 2000
END_YEAR = 2022

# mapping of feature codes to more meaningful names
featureMap={
    'NY.GDP.PCAP.PP.CD': 'GDP per capita in USD', 
    'NY.GDP.MKTP.KD.ZG': 'GDP per capita growth' 
    #'SL.EMP.SELF.ZS': 'Self-employment (%)',
    #'EG.FEC.RNEW.ZS': 'Renewable Energy Consumption (%)',
    #'NE.TRD.GNFS.ZS': 'Trade (% of GDP)',
    #'BX.KLT.DINV.WD.GD.ZS': 'FDI (as % of GDP)',
    #'SL.EMP.VULN.FE.ZS': 'Vulnerable employment (% of employment)'
}

# Mapping of country codes to their actual names
countryMap={
    "US": "USA",
    "IN":"India",
   "CN": "China"
}

# constant parameters used in sending the request.
params = dict()
# to ensure we receive a JSON response
params['format']='json'
# The data we fetch is for 59 years.
# Hence we change the default page size of 50 to 100 to ensure we need only one API call per feature.
params['per_page']='100'
# Range of years for which the data is needed
params['date']=(f"{START_YEAR}:{END_YEAR}")


#---------------------------------------BACKUP-------------------------------------------------------------

#Create a dataframe holding all the country data 
df_list = []

#Base URL used in all the API calls
BASE_URL='http://api.worldbank.org/v2/'

# Function to get JSON data from the endpoint
def loadJSONData(country_code): 

    data_list=[]
    
    # iterate over each indicator code specified in the contant INDICATOR_CODES defined above
    for indicator in INDICATOR_CODES: 
        
        # form the URL in the desired format
        # E.g: http://api.worldbank.org/v2/countries/us/indicators/SP.POP.TOTL?format=json&per_page=200&date=2000:2020
        url=BASE_URL+'country/'+country_code.lower()+'/indicator/'+indicator
        

        # send the request using the resquests module
        response = requests.get(url, params=params)
        
        # validate the response status code
        # The API returns a status_code 200 even for error messages,
        # however, the response body contains a field called "message" that includes the details of the error
        # check if message is not present in the response
        if response.status_code == 200 and ("message" not in response.json()[0].keys()):
            print("Successfully got data for: " + str(featureMap[indicator]))
            
            # list of values for one feature
            indicator_values=[]
            
            # the response is an array containing two arrays - [[{page: 1, ...}], [{year: 2018, SP.POP.TOTL: 123455}, ...]]
            # hence we check if the length of the response is >1
            if len(response.json()) > 1:
                
                # if yes, iterate over each object in the response
                # each object gives one single value for each year
                for obj in response.json()[1]:
                    
                    # check for empty values
                    if obj['value'] == "" or obj['value'] is None:
                        indicator_values.append(None)

                    else:
                    # if a value is present, add it to the list of indicator values
                        indicator_values.append(float(obj['value']))
                data_list.append(indicator_values)
        else:
            # print an error message if the API call failed
            print("Error in Loading the data. Status Code: " + str(response.status_code))
            
    # Once all the features have been obtained, add the values for the "Year"
    # The API returns the indicator values from the most recent year. Hence, we create a list of years in reverse order
    data_list.append([year for year in range(END_YEAR+1, START_YEAR, -1)])
    # return the list of lists of feature values [[val1,val2,val3...], [val1,val2,val3...], [val1,val2,val3...], ...]
    return data_list

#----------------------------------------------------------------------------------------------------

# function to invokde the loadJSONData function and form the final DataFrame for each country
def getCountrywiseDF(country_code):
    
    # The resulting dataframe needs to have meaningful column names
    # hence we create a list of column names from the map defined above
    col_list=list(featureMap.values())
    # append the year column name
    col_list.append('Year')

    print("------------------Loading data for: "+countryMap[country_code]+"-----------------------")
    
    # for the given country call the loadJSONData function and fetch the data from the API
    data_list=loadJSONData(country_code)

    # transform the list of lists of features into a DataFrame
    # np.column_stack is used to add each list as a column 
    df=pd.DataFrame(np.column_stack(data_list), columns=col_list)
   
    # add the country column by extracting the country name from the map using the country code
    df['Country'] = countryMap[country_code]
    
    # display the resulting dataframe
    #print(df.head())
    
    # return the formed dataframe for the given country
    return df

# Call the getCountrywiseDF function with the code of each country under consideration

for key, value in countryMap.items(): 
    country_df = getCountrywiseDF(key)
    df_list.append(country_df)

# Combine dataframes into one 
df_combined = pd.concat(df_list)
print(df_combined.head(50))

print("Data Loading Completed")

# Save dataframe as csv file 
df_combined.to_csv('wb_data.csv', index=False)
