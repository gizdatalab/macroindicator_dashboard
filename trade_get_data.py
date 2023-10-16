import pandas as pd 
from api_functions.wb_data import get_wb_data

########################### SPECIFY START AND END YEAR ###############################

START_YEAR = 2000
END_YEAR = 2023

########################### SPECIFY THE WB INDICATORS NEEDED ##########################

featureMap_indicators={
    'NE.EXP.GNFS.CD': 'Exports of goods and services (current US$)',
    'NE.IMP.GNFS.CD': 'Imports of goods and services (current US$)',
    'TX.VAL.MRCH.CD.WT': 'Merchandise exports (current US$)', 
    'BX.GSR.NFSV.CD': 'Service exports (BoP, current US$)', 
    'NE.TRD.GNFS.ZS': 'Trade (% of GDP)',
    'LP.LPI.OVRL.XQ': 'Logistics performance index: Overall (1=low to 5=high)',
    'LP.LPI.CUST.XQ': 'Logistics performance index: Efficiency of customs clearance process (1=low to 5=high)',
    'LP.LPI.INFR.XQ':'Logistics performance index: Quality of trade and transport-related infrastructure (1=low to 5=high)',
    'TM.TAX.MRCH.WM.AR.ZS':'Tariff rate, applied, weighted mean, all products (%)'
}

########################### RETRIEVE DATA ##########################

# World Bank 
df_trade = get_wb_data(featureMap_indicators, START_YEAR, END_YEAR)
print(df_trade)

# Save as excel file
df_trade.to_excel('data/trade_data.xlsx', index=False)