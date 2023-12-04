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
    label="Choose your country of interest",
    options=df_countries
    )

# DESCRIPTION REGIONS/PEER COUNTRIES
st.sidebar.caption("""If you want to compare the values of the chosen country
                   to peer countries, please make a selection below.""")

# PEER COUNTRY INPUT WIDGET
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

st.sidebar.download_button(label="Download full data as csv file",
                   data=csv, 
                   file_name='production_data.csv')

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
st.title("Production Indicators")

st.write("""
        This dashboard provides a holistic 
        overview of the economic situation in different countries, using the most important 
        macroeconomic indicators for production. The data displayed 
        is derived from reputable international organizations. More information can be found 
        in the data sources tab below. This interactive platform allows users to get a quick 
        overview of the current production situation in different 
        countries while taking a gender perspective and allowing for comparison with peer countries. 
         """)


# Add the info box
with st.expander("ℹ️ - About the data sources", expanded=False):
    st.write(
        """
        <ul>
        <li>World Bank. “GDP, PPP (constant 2017 international $).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NY.GDP.MKTP.PP.KD.</li> 
        <li>World Bank. “GDP per capita, PPP (constant 2017 international $).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD.</li> 
        <li>World Bank. “Population, total.” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/SP.POP.TOTL.</li> 
        <li>World Bank. “Population growth (annual %).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/SP.POP.GROW.</li> 
        <li>International Monetary Fund. “Capital stock at constant 2011 national prices (in bil. 2011US$).” IMF Private and Public Capital Stock Dataset (PGCS), International Monetary Fund, 2017, dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/PGCS/A..rnna.?.</li> 
        <li>International Monetary Fund. “Growth rate in total capital stock (%).” IMF Private and Public Capital Stock Dataset (PGCS), International Monetary Fund, 2017, dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/PGCS/A..rnna_pch.?.</li>
        </ul> 
        """,unsafe_allow_html=True)
    

############################ ROW 1 ###################################

st.subheader("")

# Display subheading 
st.subheader("Everyone is talking about  Gross Domestic Product (GDP) - but what does it actually mean?")
st.subheader("")


# Configure columns
col1, col2, col3 = st.columns([1,0.02,1])

with col1:
    
    with col1: 

    #### Explanatory text box 1
        st.markdown("""<div style="text-align: justify;">The best way to understand GDP is probably
                    by breaking it down into its components. Let us start with <strong>Product</strong>: 
                    The GDP measures all <em>final goods</em> and <em>services</em> that 
                    have been produced within a defined time period (typically a year).  If this year, 
                    someone sells a house that has been build two years ago, it will not be part of 
                    this year's GDP. Also, if someone resells a car that has been both, manufactured 
                    and bought this year, it will only be counted once 
                    into GDP since reselling is not producing.</div> 
                    <br>
                    <div style="text-align: justify;">Examples for <strong>services</strong> are a haircut, entertainment, a taxi ride, 
                    consultancy, a craft activity, renting out an apartment, formal schooling, or health care. 
                    They all have in common that you cannot store them. <strong>Goods</strong>, in turn, can 
                    be stored as they are tangible things such as food, clothes, books, 
                    computers, mobiles, machines in general, and even buildings.  What does the term <strong>final</strong> 
                    mean? A car is a final good – but the steel and glass a car manufacturer buys to produce 
                    the car are not final goods. That is: All the goods and services which directly end up 
                    in a product are not final goods. Machines, however, are final goods since they are used 
                    to produce goods, but do not directly end up in them. <strong>Domestic</strong>: Only those 
                    final goods and services are part of the GDP that are produced 
                    in the considered country. Whether a domestic factory belongs to a foreign owner or 
                    a domestic one does not matter - it only matters that the good is produced in the regarded country.</div>""", unsafe_allow_html=True
        )

    st.header("")

#### Graph 1

with col3: 

    # Create tabs 
    tab1, tab2 = st.tabs(['GDP per capita', 'GDP'])

    with tab1: 

        # Title
        st.subheader("")
        st.markdown(f"""<div style="text-align: justify;"><b>Chart 1 - GDP per capita for {selected_country}</div></b>""", unsafe_allow_html=True)

        # Get data
        chart1_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['GDP per capita'])

        # ### Group data by year
        chart1_data = chart1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

        # Configure plot
        fig = px.line(chart1_data,
                        x="Year", 
                        y="Value",   
                        color='Country',
                        #title='Chart 1 - GDP per capita (constant 2017 international $)',
                        hover_name="Value",
                        color_discrete_sequence=px.colors.qualitative.Plotly,
                        labels={
                        "Value": "US Dollar (constant 2017 international $)",
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
        
        # Fix y-axis to zero and add margin
        fig.update_yaxes(range = [0, ((max(chart1_data.Value))*1.2)])

        # Display graph
        st.plotly_chart(fig, use_container_width=True)

        # Subtitle
        st.caption("Data Source: World Bank (for more information see data sources tab above)")
        st.header("")

        # Caption graph
        #st.caption('Data Sources: World Development Indicators (WDI)')
    
    with tab2: 
        
        # Title
        st.subheader("")
        st.markdown(f"""<div style="text-align: justify;"><b>Chart 2 - GDP for {selected_country}</div></b>""", unsafe_allow_html=True)
        
        # Get data
        chart2_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['GDP'])

        # ### Group data by year
        chart2_data = chart2_data.groupby([chart2_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
       
        # Configure plot
        fig = px.line(chart2_data,
                        x="Year", 
                        y="Value",   
                        color='Country',
                        #title = 'Chart 2 - GDP (constant 2017 international $)',
                        hover_name="Value",
                        color_discrete_sequence=px.colors.qualitative.Plotly,
                        labels={
                        "Value": "US Dollar (constant 2017 international $)",
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
        
        # Fix y-axis to zero and add margin
        fig.update_yaxes(range = [0, ((max(chart2_data.Value))*1.2)])

        # Display graph
        st.plotly_chart(fig, use_container_width=True)

        # Subtitle
        st.caption("Data Source: World Bank (for more information see data sources tab above)")
        st.header("")
        
        # Caption graph
        #st.caption('Data Source: World Development Indicators (WDI)')


############################# ROW 2 ###################################

# Text 
st.subheader("So how do people actually manage that their economies grow?")
st.header("")

# Configure columns
col1, col2, col3 = st.columns([1,0.02,1])

with col1:
    
    st.markdown("""<div style="text-align: justify;">In chart 1, we can see that 
                the economies of a lot of countries (if selected) tend to grow. That is, 
                year by year most countries manage to establish new "high scores" in terms 
                of the total value of final goods and services they have produced in that 
                year (GDP). <strong>So how do people actually manage that their economies grow?</strong></div>  
                <br>
                <div style="text-align: justify;">Production depends on three so-called factors of production: Economists 
                call the first <strong>land</strong> – which is a synonym for natural resources. They 
                provide the material input for all the goods and services that an economy 
                produces. Obviously, the material boundaries of our planet set an upper 
                limit for material growth on earth.</div>   
                <br>
                <div style="text-align: justify;">The second factor is <strong>capital</strong>: Capital are all those products that can 
                be used to produce further products and do not end up in them: machines, 
                tools and equipment, patents, buildings, a country's infrastructure. The 
                more of these products are available, the more goods and services an economy 
                can produce. Or, in turn, without any factories there will not be any industrial 
                products. Hence, increasing the capital stock is one way to make an economy grow.</div>  
                <br>
                <div style="text-align: justify;">The last and third factor of production is <strong>labour</strong>. Labour is provided by people. 
                That means, if the population is growing, there are more people around who can work. Thus, usually, an economy grows when its population is growing (for more 
                information on employment, check out our other <a href="https://employment-dashboard.streamlit.app/">employment dashboard)</a>).
                </div>""", unsafe_allow_html=True
        )    
    
    st.subheader("")
    
with col1:
                
    st.markdown("""<div style="text-align: justify;">Besides the pure quantity of people and capital items around, the 
                <strong>quality</strong> of 
                both factors matters as well: If people are better educated and trained they 
                will, most likely, be able to work more efficient and will consequently produce 
                more per hour than before. In this context, one also often refers to the 
                term “human capital”</div>
                <br>
                <div style="text-align: justify;">What education is to humans, innovation (or science) is 
                to capital: If the same number of machines and production processes suddenly 
                function with a more efficient technology, due to an innovation, then again 
                production increases – thus, the economy grows.</div>""", unsafe_allow_html=True
        )


### Chart Population ###

with col3: 

    # Title
    st.markdown(f"""<div style="text-align: justify;"><b>Chart 3 - Total Population of {selected_country}</div></b>""", unsafe_allow_html=True)
    
    # Get data
    chart3_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Total population'])

    # ### Group data by year
    chart3_data = chart3_data.groupby([chart3_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
          
    # Configure plot
    fig = px.line(chart3_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    #title='Chart 3 - Total Population',
                    hover_name="Value",
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    labels={
                        "Value": "Number of people",
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
    
    # Fix y-axis to zero and add margin
    fig.update_yaxes(range = [0, ((max(chart3_data.Value))*1.5)])

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption("Data Source: World Bank (for more information see data sources tab above)")
    st.header("")


### Chart Capital ###

with col3:

    # Title
    st.markdown(f"""<div style="text-align: justify;"><b>Chart 4 - Capital stock in {selected_country}</div></b>""", unsafe_allow_html=True) 
    
    # Get data
    chart4_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Capital stock (in bil. 2011US$)'])

    # Group data by year
    chart4_data = chart4_data.groupby([chart4_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
        
    # Configure plot
    fig = px.line(chart4_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    hover_name="Value",
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    labels={
                        "Value": "US Dollar (in bil. 2011US$)",
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
    
    # Fix y-axis to zero and add margin
    fig.update_yaxes(range = [0, ((max(chart4_data.Value))*1.5)])

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Subtitle
    st.caption("Data Source: IMF (for more information see data sources tab above)")
    st.subheader("")


### Chart Annual Growth Rates ###

# Title
st.markdown(f"""<div style="text-align: justify;"><b>Chart 5 - {selected_country}'s Annual Growth Rates [%]</div></b>""", unsafe_allow_html=True) 
  
# Get data
chart5_data = get_filtered_data([selected_country], selected_start_year, selected_end_year, ['Population Growth Rate', 'GDP Growth', 'Growth rate in total capital (%)'])

# ### Group data by year
chart5_data = chart5_data.groupby([chart5_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

# Configure plot
fig = px.line(chart5_data,
                x="Year", 
                y="Value",   
                color='Indicator',
                #title=f"Chart 5 - {selected_country}'s Annual Growth Rates [%]",
                hover_name="Value",
                color_discrete_sequence=px.colors.qualitative.Plotly,
                labels={
                    "Value": "Percentage",
                }
                )

# Move legend 
fig.update_layout(legend=dict(
    #orientation="h",
    yanchor="bottom",
    y=-0.6,
    xanchor="left",
    x=-0.05
    ))

# Fix y-axis to zero and add margin
fig.update_yaxes(range = [((min(chart5_data.Value))*1.2), ((max(chart5_data.Value))*1.2)])

# Update legend names
newnames = {'Population Growth Rate': 'Population growth rate', 
            'GDP Growth': 'GDP growth rate', 
            'Growth rate in total capital (%)': 'Total capital growth rate (%)'}

fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
# Fix y-axis to zero and add margin
if (min(chart5_data.Value)) < 0:
    fig.update_yaxes(range = [((min(chart5_data.Value)) - 5), ((max(chart5_data.Value)) + 5)])
else:
    fig.update_yaxes(range = [((min(chart5_data.Value)) + 5), ((max(chart5_data.Value)) + 5)])



# Display graph
st.header("")
st.plotly_chart(fig, use_container_width=True)

# Subtitle
st.caption(f"Data Sources: World Bank, IMF (for more information see data sources tab above)")
st.subheader("")
