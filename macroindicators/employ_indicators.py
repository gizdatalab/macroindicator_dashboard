import pandas as pd 

from api_functions.wb_data import get_wb_data
from api_functions.ilo_data import get_ilo_data

########################### SPECIFY START AND END YEAR ###############################

START_YEAR = 2000
END_YEAR = 2025

########################### SPECIFY THE WB INDICATORS NEEDED ##########################

featureMap_indicators={
    'SP.POP.TOTL': 'Total population',
    'SP.POP.TOTL.FE.IN': 'Total population, female',
    'NV.AGR.TOTL.ZS': 'GDP Share Agriculture (%)', 
    'NV.IND.TOTL.ZS': 'GDP Share Industry (%)', 
    'NV.SRV.TOTL.ZS': 'GDP Share Services (%)',
    'NY.GDP.MKTP.PP.KD': 'GDP, PPP (constant 2017 international $)'
}

########################### SPECIFY THE ILO INDICATORS NEEDED ##########################

# Initialize an empty dictionary to store indicators and their parameters

INDICATORS_ILO = {}

# Adding parameters for indicators (Note: online there is always an '_A' added at the end of each indicator, needs to be taken out to work)
# Indicator ids can be found here: https://ilostat.ilo.org/data/
INDICATORS_ILO['Population by sex and age'] = {'indicator': 'POP_2POP_SEX_AGE_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Labour force by sex age'] = {'indicator': 'EAP_TEAP_SEX_AGE_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Employment by sex and age'] = {'indicator': 'EMP_TEMP_SEX_AGE_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Labour force participation rate by sex and age'] = {'indicator': 'EAP_DWAP_SEX_AGE_RT', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Unemployment rate by sex and rate'] = {'indicator': 'UNE_DEAP_SEX_AGE_RT', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Population in working age, female'] = {'indicator': 'POP_2POP_SEX_AGE_NB', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Labour force, female share'] = {'indicator': 'EAP_TEAP_SEX_AGE_NB', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Employment, female share'] = {'indicator': 'EMP_TEMP_SEX_AGE_NB', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
INDICATORS_ILO['Youth unemployment'] = {'indicator': 'UNE_DEAP_SEX_AGE_RT', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_Y15-24'}
INDICATORS_ILO['Youth unemployment, female share'] = {'indicator': 'UNE_DEAP_SEX_AGE_RT', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_Y15-24'}
INDICATORS_ILO['Employment Agriculture'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_A'}
INDICATORS_ILO['Employment Mining and quarrying'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_B'}
INDICATORS_ILO['Employment Manufacturing'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_C'}
INDICATORS_ILO['Employment Utilities'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_D'} ### NOT SURE IF CORRECT; DOUBLE CHECK! 
INDICATORS_ILO['Employment Construct'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_F'}
INDICATORS_ILO['Employment Wholesale'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_G'}
INDICATORS_ILO['Employment Transport'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_H'} ### NOT SURE IF CORRECT; DOUBLE CHECK! 
INDICATORS_ILO['Employment Accomodation'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_I'}
INDICATORS_ILO['Employment Financial'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_K'}
INDICATORS_ILO['Employment Real estate'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_L'}
INDICATORS_ILO['Employment Public administration and defence'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_O'}
INDICATORS_ILO['Employment Education'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_P'}
INDICATORS_ILO['Employment Human health and social work activities'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_Q'}
INDICATORS_ILO['Employment Other services'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_S'}

# Specify all the parameters used (necessary because they need to be removed from indicator code at some point)

PARAMS_USED = ['SEX', 'AGE', 'ECO']

# Parameters 
# Define featureMap for parameters 
featureMap_params = {
    'SEX_T': 'Total',
    'SEX_F': 'Female',
    'AGE_YTHADULT_Y15-64': 'Age (Youth, adults): 15+',
    'AGE_YTHADULT_Y15-24': 'Age (Youth, adults): 15-24', 
    'ECO_ISIC4_A': 'Economic activity (Detailed): Agriculture; forestry and fishing ~ISIC rev.4 A',
    'ECO_ISIC4_B': 'Economic activity (Detailed): Mining and quarrying ~ISIC rev.4 B',
    'ECO_ISIC4_C': 'Economic activity (Detailed): Manufacturing ~ISIC rev.4 C',
    'ECO_ISIC4_D': 'Economic activity (Detailed): Utilities ~ISIC rev.4 D; E',
    'ECO_ISIC4_F': 'Economic activity (Detailed): Construction ~ISIC rev.4 F',
    'ECO_ISIC4_G': 'Economic activity (Detailed): Wholesale and retail trade; repair of motor vehicles and motorcycles ~ISIC rev.4 G',
    'ECO_ISIC4_H': 'Economic activity (Detailed): Transport; storage and communication ~ISIC rev.4 H; J',
    'ECO_ISIC4_I': 'Economic activity (Detailed): Accommodation and food service activities ~ISIC rev.4 I',
    'ECO_ISIC4_K': 'Economic activity (Detailed): Financial and insurance activities ~ISIC rev.4 K',
    'ECO_ISIC4_L': 'Economic activity (Detailed): Real estate; business and administrative activities ~ISIC rev.4 L; M; N',
    'ECO_ISIC4_O': 'Economic activity (Detailed): Public administration and defence; compulsory social security ~ISIC rev.4 O',
    'ECO_ISIC4_P': 'Economic activity (Detailed): Education ~ISIC rev.4 P',
    'ECO_ISIC4_Q': 'Economic activity (Detailed): Human health and social work activities ~ISIC rev.4 Q',
    'ECO_ISIC4_S': 'Economic activity (Detailed): Other services ~ISIC rev.4 R; S; T; U',

}


########################### RETRIEVE THE DATA ##########################

# World Bank 
wb_data = get_wb_data(featureMap_indicators, START_YEAR, END_YEAR)
#wb_data.to_csv('data/employment_data/wb_data.csv', decimal='.', index=False)

# ILOSTAT
ilo_data = get_ilo_data(INDICATORS_ILO, START_YEAR, END_YEAR, PARAMS_USED, featureMap_params)
#ilo_data.to_csv('data/employment_data/ilo_data.csv', index=False)

# Concat dataframes and append country classifications
df_employ = pd.concat([wb_data, ilo_data])

# Drop the unnecessary columns 
df_employ.drop(columns={'M49 Code', 'ISO-alpha2 Code', 'WEO Country Code'}, inplace=True)

# # Make sure data has the right type 
# list_of_int = ['Least Developed Countries (LDC)', 
#            'Land Locked Developing Countries (LLDC)', 
#            'Small Island Developing States (SIDS)',
#            'High income',
#            'Low income', 
#            'Lower middle income',
#            'Upper middle income', 
#            'WEO Country Code',
#            'M49 Code']
#
#df_employ[list_of_int] = df_employ[list_of_int].astype('int')

# Save as excel file
df_employ.to_excel('data/employment_data.xlsx', index=False)

print(df_employ)

