import pandas as pd 

from api_functions.wb_data import get_wb_data
from api_functions.imf_data import get_imf_data

from prod_params import START_YEAR, END_YEAR, featureMap_indicators_wb, featureMap_indicators_imf, DATASET


########################### RETRIEVE THE DATA ##########################

# World Bank 
wb_data = get_wb_data(featureMap_indicators_wb, START_YEAR, END_YEAR)

# IMF 
imf_data = get_imf_data(featureMap_indicators_imf, START_YEAR, END_YEAR, DATASET)


########################### MANUALLY CALCULATE GDP GROWTH ##########################

# Step 1: Create an empty list to store new rows
new_rows = []

# Step 2-3: Iterate through each row in the dataframe
for index, row in wb_data.iterrows():

    if row['Indicator Code'] == 'NY.GDP.MKTP.PP.KD':  # Check if indicators column has the desired value
        country = row['Country Code']
        year = row['Year']
        prev_year = year - 1

        # Find the corresponding row from the previous year
        prev_year_row = wb_data[(wb_data['Country Code'] == country) & 
                                (wb_data['Year'] == prev_year) & 
                                (wb_data['Indicator Code'] == 'NY.GDP.MKTP.PP.KD')]

        if not prev_year_row.empty:
                prev_year_value = prev_year_row['Value'].values[0]
                current_value = row['Value']

                # Calculate the new value based on the formula
                new_value =((current_value / prev_year_value) - 1) * 100
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

# Calculate region values for the indicators and attach to df

selected_cols  = ['Region', 'Income Group', 'Least Developed Countries (LDC)', 
                  'Land Locked Developing Countries (LLDC)', 
                  'Small Island Developing States (SIDS)']

for ele in selected_cols: 
    mean_values = df_prod.groupby([ele , 'Indicator', 'Year'])['Value'].mean().reset_index()
    mean_values = mean_values[~(mean_values[ele] == 0)]
    df_prod = pd.concat([df_prod, mean_values])

# Save as excel file
df_prod.to_excel('data/production_data.xlsx', index=False)