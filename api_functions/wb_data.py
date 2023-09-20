#SOURCE: https://pypi.org/project/wbgapi/

import wbgapi as wb
import pandas as pd

#-------------------------------------- WB PARAMETERS---------------------------------------------

# Define the indicators needed here (code from WB page, name will be shown in dataset)

# featureMap_indicators={
#     'NV.AGR.TOTL.ZS': 'GDP Share Agriculture (%)', 
#     'NV.IND.TOTL.ZS': 'GDP Share Industry (%)', 
#     'NV.SRV.TOTL.ZS': 'GDP Share Services (%)',
#     'NY.GDP.MKTP.PP.KD': 'GDP, PPP (constant 2017 international $)',
#     'SP.POP.TOTL': 'Total population',
#     'SP.POP.GROW': 'Population growth (annual %)'
# }

# # Define start and end year
# START_YEAR = 2020
# END_YEAR = 2022

#--------------------------------------FUNCTION---------------------------------------------


def get_wb_data(feature_map_input, start_year_input, end_year_input):

    """
    Function that takes a list of indicator codes as an input and retrieves the
    values through the world bank API. The output is a dataframe and a csv file of the data 
    that is stored in the directory.  

    """

    ################################### Access data through API #####################################

    # Create a list of all indicators used retrieved from the featureMap

    list_of_indicators = []
    for key, value in feature_map_input.items(): 
        list_of_indicators.append(key)

    # Retrieve data for all indicators

    df = wb.data.DataFrame(list_of_indicators, time=range(start_year_input, end_year_input), skipBlanks=True, columns='series', labels=True).reset_index()

    ################################### Process data #####################################

    # Change the column names 
    df.rename(columns={"economy": "Country Code", "MEASURE": "Indicator Code", "Time": "Year"}, inplace=True)

    # Drop redundant columns 
    df.drop(columns=["time"], inplace=True)

    # Ensure years are in the right format (integer)
    df['Year'] = df['Year'].astype('int')

    # Transform the dataframe from wide format into long format 
    df = pd.melt(df, #dataframe name
                id_vars=['Country Code', 'Country', 'Year'], #id values to keep as columns 
                value_vars=list(feature_map_input.keys()), #list of columns to melt into one column
                var_name='Indicator Code', #column name for column that stores the names of value_vars
                value_name='Value') #column name for column that stores the values of value_vars

    # Add column of indicator ids
    df['Indicator'] = df['Indicator Code'].map(feature_map_input)

    # Round indicator values to two decimals behind comma 
    df['Value'] = df['Value'].round(2)

    # Reorder columns 
    df = df[['Country Code', 'Indicator Code', 'Indicator', 'Year', 'Value']]

    # Add country and region columns
    df_country_codes = pd.read_excel('country_classifications/country_codes.xlsx')
    df_country_codes.rename(columns={'ISO-alpha3 Code': 'Country Code', 'Region Name': 'Region', 'Sub-region Name': 'Sub-region'}, inplace=True)
    df = pd.merge(df, df_country_codes, on=['Country Code'], how="left")

    # Drop all regions and entries that are not countries
    df = df.dropna(subset=['Country'])

    # Rearrange and drop unnecessary columns
    df = df[['Country Code', 'Country', 'Indicator Code', 
                       'Indicator', 'Year', 'Value', 'Region', 'Sub-region', 'Income Group',
                       'Least Developed Countries (LDC)', 'Land Locked Developing Countries (LLDC)',
                       'Small Island Developing States (SIDS)']]

    # Save as excel file 
    #df.to_excel('data\wb_data.xlsx', index=False)

    return df

#print(get_wb_data(featureMap_indicators, START_YEAR, END_YEAR))