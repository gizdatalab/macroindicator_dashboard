import pandas as pd 

df_UNSD_class = pd.read_excel('country_classifications/UNSD — Methodology.xlsx')
df_imf_class = pd.read_excel('country_classifications/imf_codes.xls.xlsx')
df_wb_class = pd.read_excel('country_classifications/world_bank_classes.xlsx')

print(df_wb_class.head())

## Process wb df
df_wb_class = df_wb_class.dropna(subset=['Income group'])
df_wb_class = df_wb_class.drop(columns={'Lending category'})
df_wb_class.rename(columns={'Code': 'ISO-alpha3 Code'}, inplace=True)

print(len(df_wb_class))
print(len(df_UNSD_class))
#pd.merge(df_UNSD_class, df_wb_class, on=['ISO-alpha3 Code'], how="left"))

## Process UNSD df 
df_UNSD_class.drop(columns={'Global Code', 'Global Name', 'Intermediate Region Code', 'Intermediate Region Name'}, inplace=True)

# Adjust income level columns 
columns_to_replace_NAN = ['Least Developed Countries (LDC)', 'Land Locked Developing Countries (LLDC)', 'Small Island Developing States (SIDS)']
df_UNSD_class[columns_to_replace_NAN] = df_UNSD_class[columns_to_replace_NAN].fillna(0)
df_UNSD_class = df_UNSD_class.replace({'x': 1})


## Process imf df 
df_imf_class.drop(columns={'WEO Subject Code', 'Country'}, inplace=True)
df_imf_class = df_imf_class.drop_duplicates()
df_imf_class.rename(columns={'ISO': 'ISO-alpha3 Code'}, inplace=True)

# #print(df_UNSD.head())
# #print(df_imf.head())
# #print(len(df_UNSD))
# #print(len(df_imf))

# Merge dataframes 
merged_df = pd.merge(df_UNSD_class, df_imf_class, on=['ISO-alpha3 Code'], how="left")
merged_df = pd.merge(merged_df, df_wb_class, on=['ISO-alpha3 Code'], how="left")

# Drop redundant columns 
merged_df.drop(columns={'Region Code', 'Sub-region Code', 'Economy', 'Region'}, inplace=True)

# Get indicator columns for the income classes 
merged_df = pd.get_dummies(merged_df, columns=['Income group'], prefix='', prefix_sep='')

print(len(merged_df))
print(merged_df[merged_df.isna().any(axis=1)])

# # Save csv file 
merged_df.to_excel('country_classifications/country_codes.xlsx', index=False)
print(merged_df.dtypes)
