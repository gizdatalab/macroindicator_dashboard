import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


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

st.sidebar.download_button(label="Download full data as csv file",
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
        <ul>
        <li>World Bank. “Exports of goods and services (current US$).” World Development Indicators, The World Bank Group, 2022, <a>data.worldbank.org/indicator/NE.EXP.GNFS.CD</a>.</li>
        <li>World Bank. “Imports of goods and services (current US$).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NE.IMP.GNFS.CD.</li> 
        <li>World Bank. “Merchandise exports (current US$).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/TX.VAL.MRCH.CD.WT.</li> 
        <li>World Bank. “Service exports (BoP, current US$).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/BX.GSR.NFSV.CD.</li> 
        <li>World Bank. “Trade (% of GDP).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NE.TRD.GNFS.ZS.</li> 
        <li>World Bank. “Logistics performance index: Efficiency of customs clearance process (1=low to 5=high).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/LP.LPI.OVRL.XQ.</li> 
        <li>World Bank. “Logistics performance index: Quality of trade and transport-related infrastructure (1=low to 5=high).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/LP.LPI.INFR.XQ.</li> 
        <li>World Bank. “Tariff rate, applied, weighted mean, all products (%).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/TM.TAX.MRCH.WM.AR.ZS.</li> 
        </ul>
        """,unsafe_allow_html=True)
    
############################# ROW 1 ###################################
st.header("")
st.subheader(f"What does {selected_country}’s trade look like? ")

col1, col2, col3 = st.columns([1,0.05,1])

with col1: 
    # Create distance
    st.header("")
    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">
                Trade is composed of exports and imports of goods and services. 
                <ul>
                <li>Exports of <b>goods</b> are goods produced <i>domestically</i> and sold to <i> a foreign country</i>. </li>
                <li>Imports of <b>goods</b> are goods produced in <i>a foreign country</i> and sold <i>domestically</i>. </li>
                <li>Exports of <b>services</b> are services provided <i>domestically</i> for a national or resident of <i>a foreign country</i>.</li> 
                <li>Similarly, imports of <b>services</b> are services provided in <i>a foreign country</i> for a 
                national or resident of <i>the domestic country</i>. </li>
                </ul>
                While trade in goods is rather intuitive, trade in services has different modes of supply and 
                can be illustrated through the following examples:                
                <ol type="i">
                <li>Tourism services are typically provided domestically for nationals or residents of a foreign country. </li>
                <li>Telecommunication services are typically provided to nationals or residents in a foreign country through 
                the foreign subsidiary of a domestic telecommunication company. </li>
                <li>Professional services such as consulting services can be provided to nationals or residents 
                in a foreign country both domestically or through the dispatch of domestic staff to the foreign country. </li>
                </ol>
                For more details on the differences between goods and services take a look at our 
                <a href="https://gdp-dashboard.streamlit.app/">production dashboard</a>. 
                High exports of goods and services are typically seen as a benchmark for success. However, exports are not an end. 
                Rather, high exports are the mean that allows a country to specialize in those sectors in which it has a relatively 
                high productivity (comparative advantage) and to purchase and consume goods and services from abroad.
                A country’s trade performance can be assessed in terms of outcomes and drivers. Outcomes measure how much is traded 
                and what the structure of trade is. Drivers measure how easy it is to trade and the extent of tariff and non-tariff 
                barriers. In chart 1, the indicator <i>trade in goods and services</i> measures total exports and respectively imports  
                in terms of their value in current US-Dollars. In chart 2, total exports can be further broken down into 
                <i>merchandise exports</i> and <i>exports of services</i>, also in terms of their value in current US-Dollars.
                </li> </div>""", unsafe_allow_html=True
    )
    

with col3: 
    # Get data
    chart1_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, 
                                    ['Exports of goods and services (current US$)', 
                                     'Imports of goods and services (current US$)'])
    chart2_data = get_filtered_data(selected_country, selected_start_year, selected_end_year,
                                    ['Merchandise exports (current US$)',
                                    'Service exports (BoP, current US$)'])
    # Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value", 
                    title= "Chart 1 - Exports and imports of goods and services",
                    color='Indicator',
                    hover_name="Value",
                    labels= {
                        "Value": "current US $"
                    }
                    )
        
    # Move legend 
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05
        ))
        
    # Fix y-axis to always show (100%)
    fig.update_yaxes(range = [0, ((max(chart1_data.Value))*1.2)])

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(chart2_data,
                    x="Year", 
                    y="Value", 
                    color='Indicator',
                    title= 'Chart 2 - Merchandise and service exports',
                    hover_name="Value",
                    labels={
                        "Value": "current US $"
                    }
                    )
        
    # Move legend 
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05
        ))
        
    # Fix y-axis to always show (100%)
    fig.update_yaxes(range = [0, ((max(chart1_data.Value))*1.2)])

    # Display graph
    st.plotly_chart(fig, use_container_width=True)
    # Caption graph
    st.caption('Data Source: World Bank (for more information see data sources tab above)')


############################# ROW 2 ###################################
st.header("")
st.subheader("How can trade openness be assessed?")

col1, col2, col3 = st.columns([1,0.05,1])

with col1:
    # Create distance
    st.header("")
    st.markdown(f"""<div style="text-align: justify;">
                A frequently used indicator for trade openness is the share of trade in gross domestic product (GDP). 
                As explained above, trade is defined as the sum of exports and imports of goods and services. 
                The indicator measures trade openness as an outcome. Factors such as barriers to trade (e.g., 
                tariffs, technical barriers to trade  such as labelling or certification requirements), 
                geographic remoteness and the size and structure of the economy influence how high or low the 
                share of trade in GDP is.
                </div>""", unsafe_allow_html=True
            )
    
with col3:
    # Get data
    chart3_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, 
                                    ['Trade (% of GDP)'])
    # Configure plot
    fig = px.line(chart3_data,
                  x="Year",
                  y="Value",
                  color='Indicator',
                  title='Chart 3 – Trade openness (in trade as % of GDP)',
                  hover_name="Value",
                  labels={
                      "Value": "Percentage"}
                      )
        
    # Move legend 
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05
        ))

    # Fix y-axis to always show (100%)
    fig.update_yaxes(range = [0, ((max(chart3_data.Value))*1.2)])

    # Display graph
    st.plotly_chart(fig, use_container_width=True)
    # Caption graph
    st.caption('Data Source: World Bank (for more information see data sources tab above)')

############################# ROW 3 ###################################
st.header("")
st.subheader("What are insights from the World Bank’s Logistics Performance Index? ")

col1, col2, col3 = st.columns([1,0.05,1])
with col1:
    # Create distance
    st.header("")
    st.markdown(f"""<div style="text-align: justify;">
                The World Bank’s <i>Logistics Performance Index (LPI)</i> ranks countries’ performance on 
                trade logistics, based on quantitative data on the performance of the logistics chain as 
                well as responses from a survey among logistics operators. The LPI is composed of six 
                sub-components, of which <i>“Efficiency of customs clearance process”</i> (e.g., speed, simplicity 
                and predictability of formalities) and <i>“Quality of trade and transport-related infrastructure”</i>  
                (e.g., ports, railroads, roads, information technology) are reported here.
                    </div>""", unsafe_allow_html=True
                )

with col3:
    # Get data
    chart4_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, 
                                    ['Logistics performance index: Overall (1=low to 5=high)'])

    chart4_data_efficiency = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year,
                                    ['Logistics performance index: Efficiency of customs clearance process (1=low to 5=high)'])

    chart4_data_quality = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year,
                                    ['Logistics performance index: Quality of trade and transport-related infrastructure (1=low to 5=high)'])

    #Graphs
    tab1, tab2, tab3 = st.tabs(["Overall", "Efficiency", "Quality"])                                
    with tab1:
        fig = px.bar(chart4_data,
                    x="Year",
                    y="Value",
                    color='Country',
                    title='Chart 4.1 – LPI: Overall (1=low to 5=high)',
                    barmode='group',
                    hover_name='Value',
                    labels={
                        'Value':'Score'
                    })
            
        # Move legend 
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="left",
            x=-0.05
            ))
            
            # Display graph
        st.plotly_chart(fig, use_container_width=True)
        # Caption graph
        st.caption('Data Source: World Bank (for more information see data sources tab above)')


    with tab2:
        fig = px.bar(chart4_data_efficiency,
                    x="Year",
                    y="Value",
                    color='Country',
                    title='Chart 4.2 – LPI: Efficiency of customs clearance <br>process (1=low to 5=high)',
                    barmode='group',
                    hover_name="Value",
                    labels={
                        'Value':'Score'
                    }
                    )
            
        # Move legend 
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="left",
            x=-0.05
            ))
            
        # Display graph
        st.plotly_chart(fig, use_container_width=True)
        # Caption graph
        st.caption('Data Source: World Bank (for more information see data sources tab above)')

    with tab3:
        fig = px.bar(chart4_data_quality,
                    x="Year",
                    y="Value",
                    color='Country',
                    title='Chart 4.3 – LPI: Quality of trade and transport-related <br>infrastructure (1=low to 5=high)',
                    barmode='group',
                    hover_name='Value',
                    labels={
                        'Value':'Score'
                    }                    
                    )
            
        # Move legend 
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="left",
            x=-0.05
            ))
        # Display graph
        st.plotly_chart(fig, use_container_width=True)

        # Caption graph
        st.caption('Data Source: World Bank (for more information see data sources tab above)')

############################# ROW 4 ###################################
st.header("")
st.subheader("How do tariffs come into play? ")

col1, col2, col3 = st.columns([1,0.05,1])
with col1:
    # Create distance
    st.header("")
    st.markdown(f"""<div style="text-align: justify;">
                The <i>trade-weighted tariff rate</i> is the weighted average tariff on imported goods. 
                The indicator is calculated by weighting each tariff of an imported good by the 
                total value (price times amount) of that good. Thereby, it is assured that those 
                tariffs on goods which are traded a lot are weighted more than tariffs on goods 
                that are barely traded. Considered are only those tariffs that are actually applied 
                by customs authorities; i.e., an exporter might avail to tariffs under WTO 
                (World Trade Organisation) rules or tariffs under the rules of a trade agreement (if there is one).
                </div>""", unsafe_allow_html=True
                )

with col3:
    # Get data
    chart5_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, 
                                    ['Tariff rate, applied, weighted mean, all products (%)'])
    fig = px.line(chart5_data,
                  x="Year",
                  y="Value",
                  color='Country',
                  title='Chart 5 – Applied trade-weighted tariff rate, <br>all products (%)',
                  hover_name="Value",
                  labels={
                      'Value': 'current US $'
                    }
                  )
            
    # Move legend 
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05,
        ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)  
    # Caption graph
    st.caption('Data Source: World Bank (for more information see data sources tab above)')
