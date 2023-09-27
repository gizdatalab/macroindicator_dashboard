import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

#---------------------------------- LOAD DATA AND PARAMETERS ---------------------------------#

# Create import function with cache (cache so data is only loaded once)
@st.cache_data
def load_data(path):
    df = pd.read_excel(path, engine='openpyxl')
    return df

# Load data 
df_income = load_data("data/income_data.xlsx")

# Get a country, region and indicator list
df_countries = df_income['Country'].unique().tolist()
df_indicators = df_income['Indicator'].unique().tolist()
df_regions = df_income['Region'].unique().tolist()
df_subregion = df_income['Sub-region'].unique().tolist()
df_sub_region = df_regions + df_subregion


# Turn years into int (str necessary first because Streamlit)
df_income['Year'] = df_income['Year'].astype(str)
df_income['Year'] = df_income['Year'].astype(int)

#------------------------------ Functions  ------------------------------------#

# Data Selection 
def get_filtered_data(country_selec, peer_selec, region_select, start_year_selec, end_year_selec, indicator_selec):

    """
    Function takes the user selection of the dashboard as an input and retrieves the
    corresponding data from the dataset. The output is a filtered dataframe. 

    """

    # Turn country, peer countries and region selection into list if not list:
    if isinstance(country_selec, str):
        country_selec = [country_selec]
    
    if isinstance(peer_selec, str):
        peer_selec = [peer_selec]
    
    if isinstance(region_select, str):
        region_select = [region_select]

    # Combine selected countries
    countries_selec = country_selec + peer_selec + region_select

    # Create a dataframe with all years and indicators first
    ## This is necessary to add the missing years with "None" values
    df_empty = pd.DataFrame([(year, indicator, country) 
                            for year in range(start_year_selec, end_year_selec+1)
                            for indicator in indicator_selec
                            for country in countries_selec],
                            columns=['Year', 'Indicator', 'Country'])

    
    # Retrieve the selected data from df
    df_fltr = df_income[(df_income['Country'].isin(countries_selec)) & 
                       (df_income['Year'] >= start_year_selec) & 
                       (df_income['Indicator'].isin(indicator_selec)) &
                       (df_income['Year'] <= end_year_selec)]
    
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
    start_year_country = int(df_income[df_income['Country'] == country_input]['Year'].min())
    end_year_country = int(df_income[df_income['Country'] == country_input]['Year'].max())

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
                   to a region or peer countries, please make a selection below.""")

# PEER COUNTRY INPUT WIDGET
selected_region = st.sidebar.multiselect(
    "Choose regions for comparison",
    df_sub_region
    )

# REGION INPUT WIDGET
selected_peer = st.sidebar.multiselect(
    "Choose peer countries for comparison",
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

csv = convert_df(df_income)

# Add empty space to create some distance 
st.sidebar.header("")

st.sidebar.download_button(label="Click here to download data as csv",
                   data=csv, 
                   file_name='income_data.xlsx')

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
st.title("Income Indicators")
st.write("""
         Explore a comprehensive income dashboard that provides a holistic view of key income indicators. 
         This interactive platform synthesizes diverse metrics, offering insights into GDP and GNI per capita, Income Shares
         of GNI per capita, Ginni coefficient, and share of population that lives with less than 6$ a day. With intuitive 
         visualizations and data-driven analysis, gain a deeper understanding of income dynamics and make informed decisions 
         for the future.
         """)


# Add the info box
with st.expander("ℹ️ - About the data sources", expanded=False):
    st.write(
        """
        Add the data sources here
        """)
    
    ############################# ROW 1 ###################################

# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

### GRAPH AND TEXT 1 ###

with col1: 

    # Display subheading 
    st.header(f"Who buys all these products in {selected_country}?")

    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">Considering the amount of goods and services produced every year, 
                one might start to ask the questions: <i> Who buys all these products? And where actually do these people 
                get all the money from? </i> To answer these questions just think about what the companies are doing with the 
                money they earn by selling newly produced products. They use it either:
                <ol type="i">
                <li>to pay a return to their owners or lenders (<i>capital share</i>)</li>
                <li>to pay wages and salaries (<i>labour share</i>)</li>
                <li>to pay other production costs.</li></ol>
                These other costs (iii) are in turn the earnings of supplying companies 
                which again distribute their earnings in the ways (i)-(iii). However, following the supply chain to its very 
                end, all earnings sooner or later flow as (i) capital share or (ii) labour share to households. Graph 1 shows 
                estimates of these two shares.</div>""", unsafe_allow_html=True
                )
    
    st.subheader("Labour income share estimates as percent of GDP")
    st.markdown("""*Note that for each country, the capital income share corresponds with the space above each country line, 
            while the labor income share with the space below.*""")


 #### Graph 1

with col1: 

    # Get data
    chart1_data = get_filtered_data(selected_country, selected_peer, selected_region, selected_start_year, selected_end_year, ['Labour income share estimates'])
    
    ### Group data by year
    chart1_data = chart1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    hover_name="Value"
                    )
    
    # Move legend 
    fig.update_layout(legend=dict(
       # orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="left",
        x=0.01
        ))
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')


with col3: 
 
    st.header(f"How's the income distributed within {selected_country}?")


    st.markdown(f"""<div style="text-align: justify;">The Gini Index measures the extent to which the distribution of 
                income among households within a country deviate from a perfectly equal distribution. A Gini Index of 0 
                represents perfect equality while an index of 100 implies perfect inequality (one person receives 100% 
                of the economy’s generated income).What the Gini Index measures can alternatively be illustrated by 
                ranking a society by its income and showing how income is allocated to five citizen groups of equal size. 
                The result of this approach is presented in chart 4. What does it say? That (in most countries) the “upper 20%” 
                of the population receives an over-proportional share of the generated income. Can 20% of a society work that 
                hard that they actually produce and should therefore gain up to 50% of the total income created by that society? 
                Consequently, can the “lowest 20%” of a society work so little that their group should receive only around 5% of GNI? 
                Chart 3 approximates what these relative values are in actual annual gross income in 2017 international $.</div>
                """, unsafe_allow_html=True
                )
    
    #st.subheader("Gini Coefficient")    

    # Get data
    chart2_data = get_filtered_data(selected_country, selected_peer, selected_region, selected_start_year, selected_end_year, ['Gini index'])
    
    ### Group data by year
    chart2_data = chart2_data.groupby([chart2_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart2_data,
                    x="Year", 
                    y="Value",   
                    color='Indicator',
                    hover_name="Value"
                    )
    
    # Move legend 
    fig.update_layout(legend=dict(
       # orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="left",
        x=0.01
        ))
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')


############################### ROW 2 ###################################

### GRAPH AND TEXT 2 ###
# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

with col1: 

    # Subheader 
    st.subheader("GNI per capita versus GDP per capita")


    #### Explanatory text box 2
    st.markdown("""<div style="text-align: justify;">If the value of the newly produced final goods and services (GDP) 
                flows as income to households, then GDP almost coincides with the income (before taxes) of the population – i.e., 
                the Gross National Income (GNI). In fact, GDP and GNI are identical in an economy in which citizens do not receive 
                some of their income from abroad. As Graph 2 shows this difference is usually relatively small. In this sense, GDP 
                per capita is a close approximation of GNI per capita and thus not only a measure of production per capita – but also 
                of the average income of a country's population.Now, if you are a full-time employee, please do not take GNI per capita 
                (or GDP per capita) as a perfect benchmark for your personal annual: Bear in mind that GNI per capita is calculated by 
                dividing GNI by the total population; however, not everyone is working full-time, and some are not working at all (e.g., 
                children). A large fraction of society is also doing unpaid work, for example childcare or home production for own use. 
                Also, GNI does not only reflect wages and salaries but also the capital share. Bearing all this in mind, GNI per capita 
                still gives you some orientation whether your gross income, and thus somehow your standard of living, is above average 
                or below.</div>""", unsafe_allow_html=True
                )
    st.header("")    

#### Graph 3
with col1: 

    # Get data
    chart3_data = get_filtered_data(selected_country, selected_peer, selected_region, selected_start_year, selected_end_year, ['GDP per capita', 'GNI per capita'])
    
    ### Group data by year
    chart3_data = chart3_data.groupby(['Indicator', 'Country'],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart3_data,
                  x='Year', 
                  y='Value',
                  color='Indicator',
                  hover_name='Country'
                  )

    # Move legend 
    fig.update_layout(legend=dict(
       # orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="left",
        x=0.01
        ))
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')


with col3: 
    #### (3) Area Chart
    st.subheader("Income Shares GNI per Capita")

    # Get data
    area1_data =  get_filtered_data(selected_country, selected_peer, selected_region, selected_start_year, selected_end_year, 
                                          ['Income share held by highest 20%', 
                                           'Income share held by second 20%',
                                           'Income share held by third 20%',
                                           'Income share held by fourth 20%',
                                           'Income share held by lowest 20%',
                                           ])


    ### Group data by year
    area1_data = area1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')


    # Configure plot
    fig = px.area(area1_data,
                  x="Year", 
                  y="Value", 
                  color='Country',
                  hover_name="Value"
                  )
    # Fix y-axis to always show (100%)
    fig.update_yaxes(range=[0, 100])

    # Move legend 
    fig.update_layout(legend=dict(
            #orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="left",
            x=0.01
            ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Subheader for poverty share
    st.subheader("Share of population that lives with less than 6$ per person a day")
    # Get data for the poverty share
    chart4_data = get_filtered_data(selected_country, selected_peer, selected_region, selected_start_year, selected_end_year, ['Poverty Share'])
    
    ### Group data by year
    chart4_data = chart4_data.groupby([chart4_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart4_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    hover_name="Value"
                    )
    
    # Move legend 
    fig.update_layout(legend=dict(
       # orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="left",
        x=0.01
        ))
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Sources: World Development Indicators (WDI)')

