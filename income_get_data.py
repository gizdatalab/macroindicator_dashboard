import pandas as pd 
from api_functions.wb_data import get_wb_data
from api_functions.ilo_data import get_ilo_data

########################### SPECIFY START AND END YEAR ###############################

START_YEAR = 2000
END_YEAR = 2025

########################### SPECIFY THE WB INDICATORS NEEDED ##########################

featureMap_indicators={
    'NY.GDP.PCAP.PP.KD': 'GDP per capita',
    'NY.GNP.PCAP.PP.KD': 'GNI per capita',
    'SI.POV.GINI': 'Gini index',
    'SI.DST.05TH.20': 'Income share held by highest 20%', 
    'SI.DST.04TH.20': 'Income share held by fourth 20%',
    'SI.DST.03RD.20': 'Income share held by third 20%',
    'SI.DST.02ND.20': 'Income share held by second 20%',
    'SI.DST.FRST.20': 'Income share held by lowest 20%',
    'SI.POV.UMIC': 'Poverty Share'
}

########################### SPECIFY THE ILO INDICATORS NEEDED ##########################

# Initialize an empty dictionary to store indicators and their parameters

INDICATORS_ILO = {}

# Adding parameters for indicators (Note: online there is always an '_A' added at the end of each indicator, needs to be taken out to work)
# Indicator ids can be found here: https://ilostat.ilo.org/data/
INDICATORS_ILO['Labour income share estimates'] = {'indicator': 'LAP_2GDP_NOC_RT'}

# Specify all the parameters used (necessary because they need to be removed from indicator code at some point)

# Parameters 
featureMap_params = {}

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

