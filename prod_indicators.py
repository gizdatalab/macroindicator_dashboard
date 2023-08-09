import pandas as pd 

from api_functions.wb_data import get_wb_data
from api_functions.imf_data import get_imf_data

########################### SPECIFY START AND END YEAR ###############################

# IMF only has data until 2017 (as of August 2023) and data retrievel doesn't work if 
# end_year > 2017 

START_YEAR = 2000
END_YEAR = 2017

########################### SPECIFY THE WB INDICATORS NEEDED ##########################

featureMap_indicators_wb={
    'NY.GDP.PCAP.PP.KD': 'GDP per capita',
    'NY.GDP.MKTP.PP.KD': 'GDP',
    'SP.POP.TOTL': 'Total population',
    'SP.POP.GROW': 'Population Growth Rate'}

########################### SPECIFY THE IMF INDICATORS NEEDED #########################

featureMap_indicators_imf = {
    'rnna': 'Capital stock (in bil. 2011US$)',
    'rnna_pch': 'Growth rate in total capital (%)'
}

# Dataset used (currently only works for one dataset at a time)
DATASET = "PGCS"

########################### RETRIEVE THE DATA ##########################

# World Bank 
wb_data = get_wb_data(featureMap_indicators_wb, START_YEAR, END_YEAR)
print(wb_data)

# IMF 
imf_data = get_imf_data(featureMap_indicators_imf, START_YEAR, END_YEAR, DATASET)
print(imf_data)

########################### MANUALLY CALCULATE GDP GROWTH ##########################

# Step 1: Create an empty list to store new rows
new_rows = []

# Step 2-3: Iterate through each row in the dataframe
for index, row in wb_data.iterrows():

    if row['Indicator Code'] == 'NY.GDP.MKTP.PP.KD':  # Check if indicators column has the desired value
        country = row['Country Code']
        year = row['Year']
        prev_year = year - 1
        #print(country)
        #print(year)
        #print(prev_year)

        # Find the corresponding row from the previous year
        prev_year_row = wb_data[(wb_data['Country Code'] == country) & 
                                (wb_data['Year'] == prev_year) & 
                                (wb_data['Indicator Code'] == 'NY.GDP.MKTP.PP.KD')]

        if not prev_year_row.empty:
                prev_year_value = prev_year_row['Value'].values[0]
                current_value = row['Value']

                # Calculate the new value based on the formula
                new_value =((prev_year_value / current_value) - 1) * 100
                new_value = round(new_value, 2)

                # Create a new row with the calculated value and all other columns from the current year's row
                new_row = row.copy()  # Copy all columns
                new_row['Year'] = year
                new_row['Value'] = new_value
                new_row['Indicator'] = 'GDP Growth'
                new_row['Indicator Code'] = 'GDP Growth'
                new_rows.append(new_row)

# Step 4-5: Append new rows to the original dataframe
wb_data = wb_data.append(new_rows, ignore_index=True)

# Concat dataframes and append country classifications
df_prod = pd.concat([wb_data, imf_data])

# Drop unnecessary columns
df_prod.drop(columns={'M49 Code', 'ISO-alpha2 Code', 'WEO Country Code'}, inplace=True)


# Save as excel file
df_prod.to_excel('data/production_data.xlsx', index=False)