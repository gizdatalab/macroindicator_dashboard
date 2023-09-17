#### URL EXAMPLES 
#EXAMPLE URL = "https://www.ilo.org/sdmx/rest/data/ILO,DF_POP_XWAP_SEX_AGE_NB/?format=jsondata&startPeriod=2020-01-01&endPeriod=2023-12-31"
#EXAMPLE URL = "https://www.ilo.org/sdmx/rest/data/ILO,DF_EMP_TEMP_SEX_AGE_NB/...SEX_T.AGE_5YRBANDS_TOTAL?startPeriod=2018&endPeriod=2020&detail=dataonly&format=jsondata"
#BASE_URL_ILO='https://www.ilo.org/sdmx/rest/data/ILO,DF_'

#HOW TO RETRIEVE SDMX METADATA AND DATA EXAMPLE: https://pandasdmx.readthedocs.io/en/latest/example.html
#CODE_LIST ILO: https://www.ilo.org/sdmx/rest/codelist?detail=allstubs
#CODE_LIST FOR SPECIFIC KEYS (CHANGE THE KEY NAME, e.g. CL_ECO -> CL_AGE): https://www.ilo.org/sdmx/rest/codelist/ILO/CL_ECO
#SDMX USER GUIDE ILO: https://www.ilo.org/ilostat-files/Documents/SDMX_User_Guide.pdf 
#FIND INDICATOR IDS HERE: https://ilostat.ilo.org/data/# 

import pandasdmx as sdmx
import pandas as pd


# #--------------------------------------ILO PARAMETERS---------------------------------------------#

# Here you define the indicators you want to retrieve and assign them a name that shows up in the dataset

# INDICATORS_ILO = {}

# # Adding parameters for indicators (Note: online there is always an '_A' added at the end of each indicator, needs to be taken out to work)
# # Indicator ids can be found here: https://ilostat.ilo.org/data/
# INDICATORS_ILO['Population'] = {'indicator': 'POP_2POP_SEX_AGE_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Labour force'] = {'indicator': 'EAP_TEAP_SEX_AGE_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Employment'] = {'indicator': 'EMP_TEMP_SEX_AGE_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Labour force participation rate'] = {'indicator': 'EAP_DWAP_SEX_AGE_RT', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Unemployment rate'] = {'indicator': 'UNE_DEAP_SEX_AGE_RT', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Population in working age, female share'] = {'indicator': 'POP_2POP_SEX_AGE_NB', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Labour force, female share'] = {'indicator': 'EAP_TEAP_SEX_AGE_NB', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Employment, female share'] = {'indicator': 'EMP_TEMP_SEX_AGE_NB', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_YGE15'}
# INDICATORS_ILO['Youth unemployment'] = {'indicator': 'UNE_DEAP_SEX_AGE_RT', 'SEX': 'SEX_T', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_Y15-24'}
# INDICATORS_ILO['Youth unemployment, female share'] = {'indicator': 'UNE_DEAP_SEX_AGE_RT', 'SEX': 'SEX_F', 'FREQ': 'A', 'AGE': 'AGE_YTHADULT_Y15-24'}
# INDICATORS_ILO['Employment Agriculture'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_A'}
# INDICATORS_ILO['Employment Mining and quarrying'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_B'}
# INDICATORS_ILO['Employment Manufacturing'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_C'}
# INDICATORS_ILO['Employment Utilities'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_D'} ### NOT SURE IF CORRECT; DOUBLE CHECK! 
# INDICATORS_ILO['Employment Construct'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_F'}
# INDICATORS_ILO['Employment Wholesale'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_G'}
# INDICATORS_ILO['Employment Transport'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_H'} ### NOT SURE IF CORRECT; DOUBLE CHECK! 
# INDICATORS_ILO['Employment Accomodation'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_I'}
# INDICATORS_ILO['Employment Financial'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_K'}
# INDICATORS_ILO['Employment Real estate'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_L'}
# INDICATORS_ILO['Employment Public administration and defence'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_O'}
# INDICATORS_ILO['Employment Education'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_P'}
# INDICATORS_ILO['Employment Human health and social work activities'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_Q'}
# INDICATORS_ILO['Employment Other services'] = {'indicator': 'EMP_TEMP_SEX_ECO_NB', 'SEX': 'SEX_T', 'FREQ': 'A', 'ECO': 'ECO_ISIC4_S'}

# #Retrieving parameters for a specific indicator
# #parameters_of_indicator1 = indicator_params.get('indicator1', {})
# #param1_value = parameters_of_indicator1.get('param1', None)

# START_YEAR = '2021'
# END_YEAR = '2023'

# # Specify all the parameters used (necessary because they need to be removed from indicator code at some point)

# PARAMS_USED = ['SEX', 'AGE', 'ECO']

# # Parameters 
# # Define featureMap for parameters 
# featureMap_params = {
#     'SEX_T': 'Total',
#     'SEX_F': 'Female',
#     'AGE_YTHADULT_Y15-64': 'Age (Youth, adults): 15+',
#     'AGE_YTHADULT_Y15-24': 'Age (Youth, adults): 15-24', 
#     'ECO_ISIC4_A': 'Economic activity (Detailed): Agriculture; forestry and fishing ~ISIC rev.4 A',
#     'ECO_ISIC4_B': 'Economic activity (Detailed): Mining and quarrying ~ISIC rev.4 B',
#     'ECO_ISIC4_C': 'Economic activity (Detailed): Manufacturing ~ISIC rev.4 C',
#     'ECO_ISIC4_D': 'Economic activity (Detailed): Utilities ~ISIC rev.4 D; E',
#     'ECO_ISIC4_F': 'Economic activity (Detailed): Construction ~ISIC rev.4 F',
#     'ECO_ISIC4_G': 'Economic activity (Detailed): Wholesale and retail trade; repair of motor vehicles and motorcycles ~ISIC rev.4 G',
#     'ECO_ISIC4_H': 'Economic activity (Detailed): Transport; storage and communication ~ISIC rev.4 H; J',
#     'ECO_ISIC4_I': 'Economic activity (Detailed): Accommodation and food service activities ~ISIC rev.4 I',
#     'ECO_ISIC4_K': 'Economic activity (Detailed): Financial and insurance activities ~ISIC rev.4 K',
#     'ECO_ISIC4_L': 'Economic activity (Detailed): Real estate; business and administrative activities ~ISIC rev.4 L; M; N',
#     'ECO_ISIC4_O': 'Economic activity (Detailed): Public administration and defence; compulsory social security ~ISIC rev.4 O',
#     'ECO_ISIC4_P': 'Economic activity (Detailed): Education ~ISIC rev.4 P',
#     'ECO_ISIC4_Q': 'Economic activity (Detailed): Human health and social work activities ~ISIC rev.4 Q',
#     'ECO_ISIC4_S': 'Economic activity (Detailed): Other services ~ISIC rev.4 R; S; T; U',

# }


#--------------------------------------FUNCTION---------------------------------------------

#Overall function to retrieve the data 

def get_ilo_data(indicators_dict, start_year_input, end_year_input, featureMap_params_input): 

    """
    Funtion to retrieve a list of indicator values from the Ilostat webpage. The output is a 
    dataframe in long format and a csv file of all indicator values.
    
    """

    ########################### Define data retrieval function #############################

    # Retrieve data for one indicator

    def access_ilo_data(indicator_id_input, indicator_name_input, params_input): 
        
        """
        Function that takes an ILOSTAT indicator code and the requested query string parameters
        to filter as an input and then retrieves the values for one specific indicator from the 
        Ilostat webpage through the API. The output is a dataframe containing the data for the 
        indicator.

        """

        # Specify the request
        ilo = sdmx.Request('ILO')

        # If parameter are specified (data filtered for age etc.)
        if params_input:
            resp = ilo.data(
                f'DF_{indicator_id_input}',
                key=params_input,
                params={'startPeriod': start_year_input, 'endPeriod': end_year_input})
        
        # If no parameters specified (data not filtered)
        else:
            resp = ilo.data(
                f'DF_{indicator_id_input}',
                params={'startPeriod': start_year_input, 'endPeriod': end_year_input})
        
        # Turn into pd dataframe
        data = resp.to_pandas()
        df = pd.DataFrame(data)
        df = df.reset_index()

        # Change the indicator code to the full code (including parameters) so that the right indicator name will be mapped
        df['MEASURE'] = indicator_id_input
        
        # Add indicator name
        df['Indicator'] = indicator_name_input

        #Change the column names 
        df.rename(columns={"REF_AREA": "Country Code", "MEASURE": "Indicator Code", "TIME_PERIOD": "Year", "value": "Value"}, inplace=True)
        df.drop(columns="FREQ", inplace=True)

        # Ensure years are in the right format (integer)
        df['Year'] = df['Year'].astype('int')

        # Rename the parameter values to full names
        if featureMap_params_input:  
            for param in params_input: 
                if param in df.columns: 
                    df[param] = df[param].map(featureMap_params_input)

        # Round indicator values to two decimals behind comma 
        df['Value'] = df['Value'].round(2)

        # Return the datframe 
        return df


    ##################################### Get data #######################################

    # Create an empty dataframe to store the data 
    df_full = pd.DataFrame()

    # Loop through each indicator in the dictionary
    for key, value in indicators_dict.items(): 

        # Retrieve the parameters
        exclude_keys = ['indicator']
        param_keys = {k: value[k] for k in set(list(value.keys())) - set(exclude_keys)}

        # Retrieve indicator key
        indicator_id = value['indicator']

        # Retrieve the indicator name 
        indicator_name = key

        # Retrieve the data for the indicator through the api 
        df_id = access_ilo_data(indicator_id, indicator_name,  param_keys)
        
        # Attach data to dataframe 
        df_full = pd.concat([df_full, df_id])
    
     # Add country and region columns
    df_country_codes = pd.read_excel('country_classifications/country_codes.xlsx')
    df_country_codes.rename(columns={'ISO-alpha3 Code': 'Country Code', 'Region Name': 'Region', 'Sub-region Name': 'Sub-region'}, inplace=True)
    df_full = pd.merge(df_full, df_country_codes, on=['Country Code'], how="left")
    
    # Drop all regions and entries that are not countries
    df_full = df_full.dropna(subset=['Country'])

    # Reorder columns 
        
    # Rearrange and drop unnecessary columns
    df_full = df_full[['Country Code', 'Country', 'Indicator Code', 
                       'Indicator', 'Year', 'Value', 'Region', 'Sub-region', 'Income Group',
                       'Least Developed Countries (LDC)', 'Land Locked Developing Countries (LLDC)',
                       'Small Island Developing States (SIDS)']]

    # Save dataframe as csv file 
    #df_full.to_excel('data\ilo_data.xlsx', index=False)

    return df_full


#print(get_ilo_data(INDICATORS_ILO, START_YEAR, END_YEAR, featureMap_params))