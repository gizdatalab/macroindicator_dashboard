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
df_prod = load_data("data/production_data.xlsx")

# Get a country, region and indicator list
df_countries = df_prod['Country'].unique().tolist()
df_indicators = df_prod['Indicator'].unique().tolist()
df_regions = df_prod['Region'].unique().tolist()
df_subregion = df_prod['Sub-region'].unique().tolist()
df_sub_region = df_regions + df_subregion

# Turn years into int (str necessary first because Streamlit)
df_prod['Year'] = df_prod['Year'].astype(str)
df_prod['Year'] = df_prod['Year'].astype(int)

# Define start and end year 
df_years = df_prod['Year'].unique().tolist()
START_YEAR = min(df_years)
END_YEAR = min(df_years)

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
    df_fltr = df_prod[(df_prod['Country'].isin(country_selec)) & 
                       (df_prod['Year'] >= start_year_selec) & 
                       (df_prod['Indicator'].isin(indicator_selec)) &
                       (df_prod['Year'] <= end_year_selec)]
    
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
    start_year_country = int(df_prod[df_prod['Country'] == country_input]['Year'].min())
    end_year_country = int(df_prod[df_prod['Country'] == country_input]['Year'].max())

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
    label="Choose country of interest",
    options=df_countries
    )

# DESCRIPTION REGIONS/PEER COUNTRIES
st.sidebar.caption("""If you want to compare the values of the chosen country
                   to peer countries, please make a selection below.""")

# PEER COUNTRY INPUT WIDGET
#selected_region = st.sidebar.multiselect(
 #   "Choose regions for comparison",
  #  df_sub_region
  #  )

# REGION INPUT WIDGET
selected_peer = st.sidebar.multiselect(
    "Choose comparison countries",
    df_countries
    )

# START AND END YEAR SLIDER 

# # Update based on data availability for chosen country 
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

csv = convert_df(df_prod)

# Add empty space to create some distance 
st.sidebar.header("")

st.sidebar.download_button(label="Click here to download data as csv",
                   data=csv, 
                   file_name='employment_data.xlsx')

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
st.title("Production dashboard")

st.write("""
         Explore a comprehensive employment dashboard that provides a holistic view of key employment indicators. 
         This interactive platform synthesizes diverse metrics, offering insights into job market trends, labor 
         force participation, and economic vitality. With intuitive visualizations and data-driven analysis, gain 
         a deeper understanding of workforce dynamics and make informed decisions for the future.
         """)


# Add the info box
with st.expander("ℹ️ - About the data sources", expanded=False):
    st.write(
        """
        Add the data sources here
        """)
    

############################ ROW 1 ###################################

# # Display subheading 
# st.subheader("Everyone is talking about  Gross Domestic Product (GDP) - but what does it actually mean? ")

# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

# ### GRAPH AND TEXT 1 ###

# with col1: 
    
#     # Text 
#     st.markdown("""<div style="text-align: justify;">The best way to understand the concept of GDP is probably
#                  by breaking it down into its components. Click through the tabs to explore the 
#                 different components.</div>""",unsafe_allow_html=True)
    
#     # Tabs 
#     tab1, tab2, tab3, tab4, tab5 = st.tabs(["Product", "Services", "Goods", "Domestic", "Gross"])

#     with tab1: 
#         st.markdown("""<div style="text-align: justify;">Let us start from the back and look at the term 
#                         <strong>"Product"</strong> first: 
#                         The GDP measures all final goods and services that have been produced within a defined time 
#                         period (typically a year).  If this year, 
#                         someone sells a house that has been build two years ago, it will not be part of 
#                         this year's GDP. Also, if someone resells a car that has been manufactured and that 
#                         she has bought this year it will only be counted once into the GDP since reselling 
#                         is not producing.</div>""",unsafe_allow_html=True)

#     with tab2: 
#         st.markdown("""<div style="text-align: justify;">Examples for <strong>"Services"</strong> are a 
#                         haircut, entertainment, a taxi ride, consultancy, a craft activity, renting out an apartment, 
#                         formal schooling, or health care. They all have in common that you cannot store them.</div>""",unsafe_allow_html=True)
    
#     with tab3: 
#         st.markdown("""<div style="text-align: justify;"><strong>"Goods"</strong>, in turn, can be stored as they are 
#                         tangible things such as food, clothes, books, computers, mobiles, machines in general, and even 
#                         buildings.  What does the term <strong>final</strong> mean? A car is a final good – but the steel and 
#                         glass a car manufacturer buys to produce 
#                         the car are not final goods. That is: All the goods and services which directly end up 
#                         in a product are not final goods. Machines, however, are final goods since they are used 
#                         to produce goods, but do not directly end up in them.</div>""",unsafe_allow_html=True)

#     with tab4: 
#             st.markdown(""" <div style="text-align: justify;">Finally, <strong>"domestic"</strong> refers to the fact
#                         that only those final goods and services are part of the GDP that are produced 
#                         in the considered country. Whether a domestic factory belongs to a foreign owner or 
#                         a domestic one does not matter - it only matters that the good is produced in the regarded country.</div>""", unsafe_allow_html=True)

with col1:

    # Display subheading 
    st.subheader("Everyone is talking about  Gross Domestic Product (GDP) - but what does it actually mean? ")
 
   
    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">The best way to understand GDP is probably
                by breaking it down into its components. Let us start with <strong>"Product"</strong>: The GDP measures all final goods and services that 
                have been produced within a defined time period (typically a year).  If this year, 
                someone sells a house that has been build two years ago, it will not be part of 
                this year's GDP. Also, if someone resells a car that has been manufactured and that 
                she has bought this year it will only be counted once into the GDP since reselling 
                is not producing.Examples for <strong>"services"</strong> are a haircut, entertainment, a taxi ride, 
                consultancy, a craft activity, renting out an apartment, formal schooling, or health care. 
                They all have in common that you cannot store them.</div> 
                <br>
                <div style="text-align: justify;"><strong>"Goods"</strong>, in turn, can be stored as they are tangible things such as food, clothes, books, 
                computers, mobiles, machines in general, and even buildings.  What does the term <strong>final</strong> 
                mean? A car is a final good – but the steel and glass a car manufacturer buys to produce 
                the car are not final goods. That is: All the goods and services which directly end up 
                in a product are not final goods. Machines, however, are final goods since they are used 
                to produce goods, but do not directly end up in them.</div>  
                <br>
                <div style="text-align: justify;"><strong>"Domestic"</strong>: Only those final goods and services are part of the GDP that are produced 
                in the considered country. Whether a domestic factory belongs to a foreign owner or 
                a domestic one does not matter - it only matters that the good is produced in the regarded country.</div>""", unsafe_allow_html=True
    )
        
    st.header("")

#### Graph 1


with col3: 

    # Get data
    chart1_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['GDP per capita'])

    # ### Group data by year
    chart1_data = chart1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

    # Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    title='Chart 1 - GDP per capita',
                    hover_name="Value",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                    )

    # # Move legend 
    # fig.update_layout(legend=dict(
    #     # orientation="h",
    #     yanchor="bottom",
    #     y=1.05,
    #     xanchor="left",
    #     x=0.01
    #     ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')

############################# ROW 2 ###################################

# Text 
st.subheader("So how do people actually manage that their economies grow?")

# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

with col1: 
    
    st.markdown("""<div style="text-align: justify;">In chart 1, we can see that 
                the economies of a lot of countries (if selected) tend to grow. That is, 
                year by year most countries manage to establish new "high scores" in terms 
                of the total value of final goods and services they have produced in that 
                year (GDP). So how do people actually manage that their economies grow?</div>  
                <br>
                <div style="text-align: justify;">Production depends on three so-called factors of production: Economists 
                call the first land – which is a synonym for natural resources. They 
                provide the material input for all the goods and services that an economy 
                produces. Obviously, the material boundaries of our planet set an upper 
                limit for material growth on earth.</div>   
                <br>
                <div style="text-align: justify;">The second factor is capital: Capital are all those products that can 
                be used to produce further products and do not end up in them: machines, 
                tools and equipment, patents, buildings, a country's infrastructure. The 
                more of these products are available, the more goods and services an economy 
                can produce. Or, in turn, without any factories there will not be any industrial 
                products. Hence, increasing the capital stock is one way to make an economy grow.</div>""", unsafe_allow_html=True
        )    
with col3:
                
    st.markdown("""<div style="text-align: justify;">The last and third factor of production is labour. Labour is provided by people. 
                That means, if the population is growing, there are more people around who can work. 
                Thus, usually, an economy grows when its population is growing (for more 
                information on employment, check out our other dashboards).</div>  
                <br>
                <div style="text-align: justify;">Besides the pure quantity of people and capital items around, the quality of 
                both factors matters as well: If people are better educated and trained they 
                will, most likely, be able to work more efficient and will consequently produce 
                more per hour than before. In this context, one also often refers to the 
                term “human capital”. What education is to humans, innovation (or science) is 
                to capital: If the same number of machines and production processes suddenly 
                function with a more efficient technology, due to an innovation, then again 
                production increases – thus, the economy grows.</div>""", unsafe_allow_html=True
        )

# Configure columns
col1, col2, col3 = st.columns([1,1,1])

### Chart GDP ###

with col1: 

  # Get data
    chart2_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['GDP'])

    # ### Group data by year
    chart2_data = chart2_data.groupby([chart2_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

    # Configure plot
    fig = px.line(chart2_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    title='Chart 2 - GDP',
                    hover_name="Value",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                    )

    # # Move legend 
    # fig.update_layout(legend=dict(
    #     # orientation="h",
    #     yanchor="bottom",
    #     y=1.05,
    #     xanchor="left",
    #     x=0.01
    #     ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')

### Chart Capital ###

with col2: 
    
  # Get data
    chart3_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Total population'])

    # ### Group data by year
    chart3_data = chart3_data.groupby([chart3_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

    # Configure plot
    fig = px.line(chart3_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    title='Chart 3 - Total Population',
                    hover_name="Value",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                    )

    # # Move legend 
    # fig.update_layout(legend=dict(
    #     # orientation="h",
    #     yanchor="bottom",
    #     y=1.05,
    #     xanchor="left",
    #     x=0.01
    #     ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')


    ### Chart Capital ###

with col3: 
    
  # Get data
    chart4_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Capital stock (in bil. 2011US$)'])

    # ### Group data by year
    chart4_data = chart4_data.groupby([chart4_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

    # Configure plot
    fig = px.line(chart4_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    title='Chart 4 - Capital stock (in bil. 2011US$)',
                    hover_name="Value",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                    )

    # # Move legend 
    # fig.update_layout(legend=dict(
    #     # orientation="h",
    #     yanchor="bottom",
    #     y=1.05,
    #     xanchor="left",
    #     x=0.01
    #     ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('International Monetary Fund (IMF)')