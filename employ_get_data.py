import pandas as pd 
from api_functions.wb_data import get_wb_data
from api_functions.ilo_data import get_ilo_data

# Import the parameters
from employ_params import START_YEAR, END_YEAR, featureMap_indicators, INDICATORS_ILO, featureMap_params

########################### RETRIEVE DATA ##########################

# World Bank 
wb_data = get_wb_data(featureMap_indicators, START_YEAR, END_YEAR)

# ILOSTAT
ilo_data = get_ilo_data(INDICATORS_ILO, START_YEAR, END_YEAR, featureMap_params)


########################### PROCESS DATA ##########################

# Multiply all values in ILO dataframe by 1000 to get normal values (except LFR and UER)
conditions = ~ilo_data['Indicator'].isin(['Labour force participation rate', 'Unemployment rate'])
ilo_data.loc[conditions, 'Value'] = ilo_data.loc[conditions, 'Value'] * 1000

# Concat dataframes and append country classifications
df_employ = pd.concat([wb_data, ilo_data])

# Calculate region values for the indicators and attach to df

selected_cols  = ['Region', 'Income Group', 'Least Developed Countries (LDC)', 
                  'Land Locked Developing Countries (LLDC)', 
                  'Small Island Developing States (SIDS)']

for ele in selected_cols: 
    mean_values = df_employ.groupby([ele , 'Indicator', 'Year'])['Value'].mean().reset_index()
    mean_values = mean_values[~(mean_values[ele] == 0)]
    df_employ = pd.concat([df_employ, mean_values])


# Save as excel file
df_employ.to_excel('data/employment_data.xlsx', index=False)



