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
PARAMS_USED = []
featureMap_params = {}

########################### RETRIEVE THE DATA ##########################

# World Bank 
wb_data = get_wb_data(featureMap_indicators, START_YEAR, END_YEAR)
#wb_data.to_csv('data/employment_data/wb_data.csv', decimal='.', index=False)

# ILOSTAT
ilo_data = get_ilo_data(INDICATORS_ILO, START_YEAR, END_YEAR, PARAMS_USED, featureMap_params)
#ilo_data.to_csv('data/employment_data/ilo_data.csv', index=False)

# Concat dataframes and append country classifications
df_income = pd.concat([wb_data, ilo_data])

# Drop unnecessary columns
df_income.drop(columns={'M49 Code', 'ISO-alpha2 Code', 'WEO Country Code'}, inplace=True)

# Save data
df_income.to_excel('data/income_data.xlsx', index=False)

print(df_income)

