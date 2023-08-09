import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Use full screen 
st.set_page_config(layout="wide")

# Import data from file 
df_employ = pd.read_excel("data/employment_data.xlsx")

# Import parameters from wb data file 
from employ_indicators import featureMap 

#---------------------------------------- MAIN PAGE ------------------------------------------------------------

# Add a title and intro text
st.title("[Test Dashboard] Macroeconomic indicators")
st.write("Macroeconomic indicators are statistical measures used to assess an economy's health and performance. They include GDP, inflation rate, unemployment rate, interest rates, and consumer spending. These indicators are crucial for policymakers, economists, and businesses to understand economic activity, price stability, labor market conditions, and future trends. By analyzing these indicators, stakeholders can make informed decisions, predict economic cycles, and compare performance internationally. In summary, macroeconomic indicators provide valuable insights into the overall state of an economy and guide decision-making processes.")

col1, col2, col3 = st.columns(3)

with col1:
   st.header('Header of Dataframe')
   st.write(df_employ.head(8))

with col2:
  st.header('Statistics')
  st.write(df_employ.describe())

############ Graph ############

with col3: 
    st.header('Plot of Data')
    st.line_chart(data=df_employ[df_employ['Country'] == "USA"], x="Year", y="GDP per capita in USD", )


# Map 
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)

# Display dataframe 
#st.table(df_wb.iloc[0:10])
#st.json({'foo':'bar','fu':'ba'})
#st.metric(label="Temp", value="273 K", delta="1.2 K")

# Create a section for the dataframe statistics
#st.header('Statistics of Dataframe')
#st.write(df_wb.describe())

# Create a section for the dataframe header
#st.header('Header of Dataframe')
#st.write(df_wb.head())

# Create a section for matplotlib figure
#st.header('Plot of Data')

# Plot graph
#st.line_chart(data=df_wb, x="Year", y="GDP per capita in USD", )

#---------------------------------------- SIDEBAR ------------------------------------------------------------


# Using object notation
add_title = st.sidebar.title("Select your data here")

#add_selectbox = st.sidebar.multiselect(
 #   "Choose your countries",
  #  COUNTRY_LIST
#)

add_selectbox = st.sidebar.multiselect(
    "Choose your indicators",
    featureMap.values()
)

add_slider = st.sidebar.slider(
    "Select the start year",
    min_value=2000, 
    max_value=2022
)

add_slider = st.sidebar.slider(
    "Select the end year",
    min_value=2000, 
    max_value=2022
)


######## Download data #########

st.sidebar.title("Get the data!")


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv_file = convert_df(df_employ)

download_button = st.sidebar.download_button(
   label='Download data as CSV', 
   data=csv_file,
   file_name='macroeconomic_indicators.csv',
   mime='text/csv'
)

#if st.download_button(...):
 #  st.sidebar.write('Thanks for downloading!')

# Add widgets to sidebar 
#st.sidebar.button
#hit_me_button = st.sidebar.radio('R:',[1,2])

# Lay out your app 
#st.form('my_form_identifier')
#st.form_submit_button('Submit to me')
#st.container()
#st.columns(spec)
#col1, col2 = st.columns(2)
#col1.subheader('Columnisation')
#st.expander('Expander')
#with st.expander('Expand'):
#     st.write('Juicy deets')



