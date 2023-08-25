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