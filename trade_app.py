import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Git checkout
# Use full screen 
st.set_page_config(layout="wide")

#---------------------------------- LOAD DATA AND PARAMETERS ---------------------------------#

# Create import function with cache (cache so data is only loaded once)
@st.cache_data
def load_data(path):
    df = pd.read_excel(path, engine='openpyxl')
    return df

# Load data 
df_trade = load_data("data/trade_data.xlsx")

# Get a country, region and indicator list
df_countries = df_trade['Country'].unique().tolist()
df_indicators = df_trade['Indicator'].unique().tolist()
df_regions = df_trade['Region'].unique().tolist()
df_subregion = df_trade['Sub-region'].unique().tolist()
df_sub_region = df_regions + df_subregion

# Turn years into int (str necessary first because Streamlit)
df_trade['Year'] = df_trade['Year'].astype(str)
df_trade['Year'] = df_trade['Year'].astype(int)


#------------------------------ Functions  ------------------------------------#

# Data Selection 

def get_filtered_data(country_selec, start_year_selec, end_year_selec, indicator_selec):

    """
    Function takes the user selection of the dashboard as an input and retrieves the
    corresponding data from the dataset. The output is a filtered dataframe. 

    """

    # Turn country selection into list if not list 
    if isinstance(country_selec, str):
        country_selec = [country_selec]

    # Create a dataframe with all years and indicators first
    ## This is necessary to add the missing years with "None" values
    df_empty = pd.DataFrame([(year, indicator, country) 
                            for year in range(start_year_selec, end_year_selec+1)
                            for indicator in indicator_selec
                            for country in country_selec],
                            columns=['Year', 'Indicator', 'Country'])

    
    # Retrieve the selected data from df
    df_fltr = df_trade[(df_trade['Country'].isin(country_selec)) & 
                       (df_trade['Year'] >= start_year_selec) & 
                       (df_trade['Indicator'].isin(indicator_selec)) &
                       (df_trade['Year'] <= end_year_selec)]
    
    ## Merge 
    df_merged = pd.merge(df_empty, df_fltr, on=['Year', 'Indicator', 'Country'], how='left')

    ## Fill other columns 
    df_merged['Indicator Code'] = df_merged.groupby('Indicator')['Indicator Code'].apply(lambda x: x.fillna(method='ffill').fillna(method='bfill'))

    for col in ['Country Code', 'Region', 'Sub-region', 'Income Group', 'Least Developed Countries (LDC)', 'Land Locked Developing Countries (LLDC)', 'Small Island Developing States (SIDS)']:
        df_merged[col] = df_merged.groupby('Country')[col].apply(lambda x: x.fillna(method='ffill').fillna(method='bfill'))

    # Turn year column into datetime format

    return df_merged

# Year Selection 
def get_years(country_input): 

    """
    Takes a country as an input and retrieves the corresponding minimum and maximum year
    available. This can be used to adjust the year slider. 

    """
    start_year_country = int(df_trade[df_trade['Country'] == country_input]['Year'].min())
    end_year_country = int(df_trade[df_trade['Country'] == country_input]['Year'].max())

    return start_year_country, end_year_country



#---------------------------------------- SIDEBAR ---------------------------------

# TITLE
add_title = st.sidebar.title("Customize your data")

# COUNTRY SELECTION INPUT WIDGET

# Specify the default options (needs to be first in list)
df_countries.remove("Germany")
df_countries.insert(0,"Germany")

# Widget
selected_country = st.sidebar.selectbox(
    label="Choose your country of interest",
    options=df_countries
    )

# DESCRIPTION REGIONS/PEER COUNTRIES
st.sidebar.caption("""If you want to compare the values of the chosen country
                   to one or more peer countries, please make a selection below.""")

# PEER COUNTRY INPUT WIDGET
#selected_region = st.sidebar.multiselect(
#    "Choose regions for comparison",
#    df_sub_region
#    )

# PEER COUNTRY INPUT WIDGET
selected_peer = st.sidebar.multiselect(
    "Choose comparison countries",
    df_countries
    )

# START AND END YEAR SLIDER 

# Update based on data availability for chosen country 
START_YEAR, END_YEAR = get_years(selected_country)

# Widget
selected_years = st.sidebar.slider(
     "Select the range",
     START_YEAR, END_YEAR, (START_YEAR,END_YEAR-1),
    )
selected_start_year = selected_years[0]
selected_end_year = selected_years[1]

# DOWNLOAD WIDGET 

# Create a csv version of the dataframe (cache so it doesn't rerun)
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df_trade)

# Add empty space to create some distance 
st.sidebar.header("")

st.sidebar.download_button(label="Download full data as csv",
                   data=csv, 
                   file_name='trade_data.csv')

st.sidebar.header("")

# INFO BOX
st.sidebar.info("""Please note that this dashboard is a prototype. 
                Users are advised that the tool may contain errors, 
                bugs, or limitations and should be used with caution 
                and awareness of potential risks, and the developers 
                make no warranties or guarantees regarding its performance, 
                reliability, or suitability for any specific purpose.""")


#---------------------------------------- MAIN PAGE --------------------------------------------

# Add a title and intro text
st.title("Trade Indicators")
st.write("""
         This dashboard provides a holistic overview of the trade situation in different
         countries, using the most important macroeconomic indicators for trade. The data 
         displayed is derived from reputable international organizations. More information can
         be found in the data sources tab below. This interactive platform allows users to get 
         a quick overview of the current trade situation in different countries while 
         allowing for comparison with peer countries. 
         """)


# Add the info box
with st.expander("ℹ️ - About the data sources", expanded=False):
    st.write(
        """
        Add the data sources here
        """)
    
############################# ROW 1 ###################################

st.header("")

# Display subheading 
st.subheader(f"Who is working in the economy in {selected_country}?")

# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])
### GRAPH AND TEXT 1 ###

with col1: 

    # Create distance
    #st.header("")

    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">
                Trade is composed of exports and imports of goods and services. 
                Exports (imports) of goods are goods produced domestically (in a foreign country) 
                and sold to a foreign country (domestically). Exports (imports) of services are services 
                provided in one country for a national or resident of a foreign country (the own country). 
                While trade in goods is rather intuitive, trade in services can be illustrated through the 
                following examples:
                <ol type="i"> 
                <li>Tourism services are typically provided domestically for nationals or residents of a foreign country </li>
                <li>Telecommunication services are typically provided to nationals or residents in a foreign country through 
                the foreign subsidiary of a domestic telecommunication company. </li>
                <li>Professional services such as consulting services can be provided to nationals or residents 
                in a foreign country both domestically or through the dispatch of domestic staff to the foreign country. </li>
                </ol>
                High exports of goods and services are typically seen as a benchmark for success. 
                However, exports are not an end. Rather, high exports are the mean that allows a country to specialize in 
                those sectors in which it has a relatively high productivity (comparative advantage) and to purchase and 
                consume goods and services from abroad.</li> </div>""", unsafe_allow_html=True
    )
    
    #st.header("")
    
    #### Graph 1

with col3: 

    # Create distance
    #st.header("")

    # Get data
    chart1_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, 
                                    ['Exports of goods and services (current US$)', 
                                     'Imports of goods and services (current US$)'])
    
    ### Group data by year
    chart1_data = chart1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value", 
                    color='Indicator',
                    hover_name="Value",
                    )
    
    # Move legend 
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="left",
        x=0.01,
        ))
    
    # Set yaxis to zero
    #fig.update_yaxes(rangemode="tozero")

    # Fix y-axis to always show (100%)
    fig.update_yaxes(range = [0, ((max(chart1_data.Value))*1.2)])
    #fig.update_layout(yaxis=dict(range=[0,max(chart1_data.Value)*1.5]))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

# Caption graph
st.caption('Data Sources: World Development Indicators (WDI)')

# Create distance
st.header("")


############################# ROW 2 ###################################