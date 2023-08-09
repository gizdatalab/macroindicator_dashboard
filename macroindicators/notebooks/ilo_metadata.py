#HOW TO RETRIEVE SDMX METADATA AND DATA EXAMPLE: https://pandasdmx.readthedocs.io/en/latest/example.html
#CODE_LIST ILO: https://www.ilo.org/sdmx/rest/codelist?detail=allstubs
#CODE_LIST FOR SPECIFIC KEYS (CHANGE THE KEY NAME, e.g. CL_ECO -> CL_AGE): https://www.ilo.org/sdmx/rest/codelist/ILO/CL_ECO
#SDMX USER GUIDE ILO: https://www.ilo.org/ilostat-files/Documents/SDMX_User_Guide.pdf 
#FIND INDICATOR IDS HERE: https://ilostat.ilo.org/data/# 

import pandasdmx as sdmx
import pandas as pd

# Specify the request
ilo = sdmx.Request('ILO')


################ CODE TO RETRIEVE METADATA ######################

# Download the metadata to check for API Codes -> can be done through this list: 
# Change the indicator ID 

metadata = ilo.datastructure('EMP_TEMP_SEX_ECO_NB')
print(metadata)

# Explore the contents of code list 
for cl in 'CL_FREQ', 'CL_SEX', 'CL_ECO':
    df_meta = sdmx.to_pandas(metadata.codelist[cl])

    #print full list of codes
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_meta)


################ CODE TO RETRIEVE DATA ######################

resp = ilo.data(
    'DF_EMP_TEMP_SEX_ECO_NB',
     key={#'SEX': 'SEX_T',
         #'FREQ': 'A', 
         'ECO': 'ECO_DETAILS_A'
       },
    params={'startPeriod': '2018', 'endPeriod': '2020'},
    )


# Turn into pandas dataframe
data = resp.to_pandas()
    #datetime={'dim': 'TIME_PERIOD', 'freq': 'freq'}).xs('Y15-74', level='age', axis=1, drop_level=False)


print(data)

################# SAVE #############################

#def get_data_ilo(indicator_id): 
#
    # Download the data
 #   resp = ilo.data(
  #      f'DF_POP_2POP_SEX_AGE_NB',
   #     key={'SEX': 'SEX_T',
    #        'FREQ': 'A', 
     #       'AGE': 'AGE_YTHADULT_Y15-64'
      #  },
       # params={'startPeriod': '2017', 'endPeriod': '2020'},
        #)
    
   # # Process data 
    #data = resp.to_pandas()
    #df = pd.DataFrame(data)
    #df = df.reset_index()


    #Change the column names 
    #df.rename(columns={"REF_AREA": "Country", "MEASURE": "ID", "TIME_PERIOD": "Year"}, inplace=True)
    #df.drop(columns="FREQ", inplace=True)

    # Return the datframe 
    #return df