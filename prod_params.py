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