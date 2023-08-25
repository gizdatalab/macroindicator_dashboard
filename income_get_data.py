import pandas as pd 
from api_functions.wb_data import get_wb_data
from api_functions.ilo_data import get_ilo_data
from income_params import START_YEAR, END_YEAR, featureMap_indicators, INDICATORS_ILO, featureMap_params


########################### RETRIEVE THE DATA ##########################

# World Bank 
wb_data = get_wb_data(featureMap_indicators, START_YEAR, END_YEAR)

# ILOSTAT
ilo_data = get_ilo_data(INDICATORS_ILO, START_YEAR, END_YEAR, featureMap_params)

########################### PROCESS DATA ##########################

# Concat dataframes and append country classifications
df_income = pd.concat([wb_data, ilo_data])

# Calculate region values for the indicators and attach to df

selected_cols  = ['Region', 'Income Group', 'Least Developed Countries (LDC)', 
                  'Land Locked Developing Countries (LLDC)', 
                  'Small Island Developing States (SIDS)']

for ele in selected_cols: 
    mean_values = df_income.groupby([ele , 'Indicator', 'Year'])['Value'].mean().reset_index()
    mean_values = mean_values[~(mean_values[ele] == 0)]
    df_income = pd.concat([df_income, mean_values])

# Save data
df_income.to_excel('data/income_data.xlsx', index=False)

print(df_income)

