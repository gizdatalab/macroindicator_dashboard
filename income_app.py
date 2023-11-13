import streamlit as st 
import pandas as pd
import plotly.express as px
import altair as alt


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
    df_fltr = df_income[(df_income['Country'].isin(country_selec)) & 
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
                   to peer countries, please make a selection below.""")


# REGION INPUT WIDGET
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
        This dashboard provides a holistic 
        overview of the economic situation in different countries, using the most important 
        macroeconomic indicators for income. The data displayed is derived from reputable 
        international organizations. More information can be found in the data sources tab 
        below. This interactive platform allows users to get a quick overview of the current
        income situation in different countries while allowing for comparison with peer countries. 
         """)


# Add the info box
with st.expander("ℹ️ - About the data sources", expanded=False):
    st.write(
        """
        <ul>
        <li>World Bank. “Population, total.” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/SP.POP.TOTL.</li>
        <li>International Labour Organization. “Population by sex and age (thousands).” ILO – Modelled Estimates, International Labour Organization, 2022, ilo.org/shinyapps/bulkexplorer4/?id=POP_2POP_SEX_AGE_NB_A.</li> 
        <li>International Labour Organization. “Labour force by sex and age (thousands).” LFS – Labour Force Survey, International Labour Organization, 2022, ilo.org/shinyapps/bulkexplorer4/?id= EAP_TEAP_SEX_AGE_NB_A.</li>
        <li>International Labour Organization. “Employment by sex and age (thousands).” LFS – Labour Force Survey, International Labour Organization, 2022, ilo.org/shinyapps/bulkexplorer4/?id= EMP_TEMP_SEX_AGE_NB_A.</li> 
        <li>International Labour Organization. “Labour force participation rate by sex and age (%).” LFS – Labour Force Survey, International Labour Organization, 2022, ilo.org/shinyapps/bulkexplorer4/?id= EAP_DWAP_SEX_AGE_RT_A.</li> 
        <li>International Labour Organization. “Unemployment rate by sex and age (%).” LFS – Labour Force Survey, International Labour Organization, 2022, ilo.org/shinyapps/bulkexplorer4/?id= UNE_DEAP_SEX_AGE_RT_A.</li> 
        <li>World Bank. “Population, female (% of total population).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/SP.POP.TOTL.FE.ZS.</li> 
        <li>World Bank. “Population, female.” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/SP.POP.TOTL.FE.IN.</li> 
        <li>International Labour Organization. “Employment by sex and economic activity (thousands).” LFS – Labour Force Survey, International Labour Organization, 2022, ilo.org/shinyapps/bulkexplorer4/?id= EMP_TEMP_SEX_ECO_NB_A.</li> 
        <li>World Bank. “Agriculture, forestry, and fishing, value added (% of GDP).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NV.AGR.TOTL.ZS.</li> 
        <li>World Bank. “Industry (including construction), value added (% of GDP).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NV.IND.TOTL.ZS.</li> 
        <li>World Bank. “Services, value added (% of GDP).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NV.SRV.TOTL.ZS.</li> 
        <li>World Bank. “GDP, PPP (constant 2017 international $).” World Development Indicators, The World Bank Group, 2022, data.worldbank.org/indicator/NY.GDP.MKTP.PP.KD.</li> 
        """, unsafe_allow_html=True)
    
############################# ROW 1 ###################################
st.header("")
st.subheader("Two sources of income: Labour and Capital")

col1, col2, col3 = st.columns([1,0.05,1])

with col1:
    # Create distance 
    st.header("")
    ### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">Considering the amount of goods and services produced 
                every year (GDP), one might start to ask the questions: <i>Who buys all these products?</i> 
                And where actually <i>do these people get all the money from?</i> To answer these questions just 
                think about what the companies are doing with the money they earn by selling newly produced 
                products: They use it either
                <ol type="i">
                <li>to pay a return to their owners or lenders (<i>capital share</i>)</li>
                <li>to pay wages and salaries (<i>labour share</i>)</li>
                <li>to pay other production costs.</li></ol>
                These other costs (iii) are in turn the earnings of supplying companies 
                which again distribute their earnings in the ways (i)-(iii). However, following the supply chain 
                to its very end, all earnings sooner or later flow as (i) capital share or (ii) labour share to 
                households. Graph 1 shows estimates of these two shares.</div>""", unsafe_allow_html=True
                )
    


 #### Graph 1

with col3: 
    # Get data
    chart1_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Labour income share estimates'])
    ### Group data by year
    chart1_data = chart1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    #Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value",   
                    color='Country',
                    hover_name="Country",
                    title= "Chart 1 - Labour income share estimates as percent of GDP",
                    labels={
                        "Value": "Percentage"
                    },
                    )
    # Add shading above and below the line
    #fig.update_traces(fill='tonexty')  # Shading below the line
    #fig.update_traces(fill='tonexty')  # Shading above the line

    #legend 
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05
        ))
    
    # Fix y-axis to zero and add margin
    fig.update_yaxes(range = [0, 100])
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""*Note that for each country, the capital income share corresponds with the space above each country line, 
            while the labor income share with the space below.*""")
    # Caption graph
    st.caption('Data Source: World Bank (for more information see data sources tab above)')

############### Row 2 ####################
st.header("")
st.subheader("Income and production – two sides of the same coin")
st.header("")
# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

with col1: 
    st.header("")
    st.markdown(f"""<div style="text-align: justify;">If the value of the <i>newly produced final goods and services (GDP)</i> flows 
                as <i>income</i> to households, then GDP <i>almost coincides with the income (before taxes) of the population – i.e.,
                the Gross National Income (GNI).</i> In fact, GDP and GNI are identical in an economy in which citizens do not 
                receive some of their income from abroad. As Chart 2 shows this difference is usually <i>relatively</i> small. 
                In this sense, GDP per capita is a close approximation of GNI per capita and thus not only a measure of 
                production per capita – but also of the <i>average income</i> of a country's population.<br>
                Now, if you are a full-time employee, please do not take GNI per capita (or GDP per capita) as a perfect benchmark 
                for your personal annual: bear in mind that GNI per capita is calculated by dividing GNI by the total population. 
                However, not everyone is working  full-time, and some are not working at all (e.g., children). A large fraction of 
                society is also doing unpaid work, for example childcare or home production for own use, which is thus not considered 
                in GNI (or GDP). Also, GNI does not only reflect wages and salaries (income from labour) but also income from capital. 
                Bearing all this in mind, GNI per capita still gives you at least some orientation whether your gross income, and thus 
                somehow your <i>standard of living</i>, is above your country’s average or below. </div>
                """, unsafe_allow_html=True
                )
    
        
with col3:
    # Get data for country and for comparison chosen
    chart2_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, ['GDP per capita', 'GNI per capita'])
    chart2_data_gdp = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['GDP per capita'])
    chart2_data_gni = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['GNI per capita'])
    
    #  Graphs
    tab1, tab2, tab3 = st.tabs([selected_country, "GDP per capita comparison", "GNI per capita comparison"])

    ### Group data by year
    chart2_data = chart2_data.groupby([chart2_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plots
    with tab1:
        fig = px.line(chart2_data,
                        x="Year", 
                        y="Value",   
                        color='Indicator',
                        title='Chart 2.1 – GDP per capita and GNI per capita',
                        labels={'Value': 'PPP current international $'},
                        hover_name="Country",
                        )
        
        # Move legend 
        fig.update_layout(legend=dict(
        # orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="left",
            x=-0.05
            ))
        
        # Display graph
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""*To allow comparison across time and between countries, 
                    all $ values are in 2017 international $ reflecting purchasing power 
                    parity (between countries) and constant prices (across time).*""")
        
        # Caption graph
        st.caption('Data Source: World Bank (for more information see data sources tab above)')

    with tab2:
        # If the peer selection is empty show error message
        if not selected_peer: 
            st.error("Please choose one or several comparison countries.")
        
        # if peer selection chosen display graph
        else:

            fig = px.line(chart2_data_gdp,
                            x="Year", 
                            y="Value",   
                            color='Country',
                            title='Chart 2.2 – Comparison of GDP per capita across the selected countries',
                            labels={'Value': 'PPP current international $'},
                            hover_name="Country",
                            )
            
            # Move legend 
            fig.update_layout(legend=dict(
            # orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="left",
                x=-0.05
                ))
            
            # Display graph
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""*To allow comparison across time and between countries, all $ values are in 2017 international $ reflecting purchasing power parity (between countries) and constant prices (across time).*""")

            # Caption graph
            st.caption('Data Source: World Bank (for more information see data sources tab above)')

    with tab3:
    # If the peer selection is empty show error message
        if not selected_peer: 
            st.error("Please choose one or several comparison countries.")
        
        # if peer selection chosen display graph
        else:
            fig = px.line(chart2_data_gni,
                            x="Year", 
                            y="Value",   
                            color='Country',
                            title='Chart 2.3 – Comparison of GNI per capita across the selected countries',
                            labels={'Value': 'PPP current international $'},
                            hover_name="Country",
                            )
            
            # Move legend 
            fig.update_layout(legend=dict(
            # orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="left",
                x=-0.05
                ))
            
            # Display graph
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""*To allow comparison across time and between countries, all $ values are in 2017 
                        international $ reflecting purchasing power parity (between countries) and constant prices (across time).*""")

            # Caption graph
            st.caption('Data Source: World Bank (for more information see data sources tab above)')



############################### ROW 3 ###################################
st.header("")
st.subheader(f"How's the income distributed within {selected_country}?")

col1, col2, col3 = st.columns([1,0.05,1])

with col1: 
    st.header("")
    #### Explanatory text box 3
    st.markdown("""<div style="text-align: justify;"> For every person above average, 
                there has to be at least one person below average. So how is income 
                <i>distributed within</i> a country? The <i>Gini Index</i> shown in chart 3 measures 
                the extent to which the distribution of income among <i>households</i> within 
                a country deviates from a perfectly equal distribution. A Gini index of 
                0 represents <i>perfect equality</i> while a score of 100 implies <i>perfect 
                inequality</i> (one person receives 100% of the economy’s generated income). 
                </div>""", unsafe_allow_html=True
                )
    
#### Graph 3
with col3:
    chart3_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Gini index'])
    
    ### Group data by year
    chart3_data = chart3_data.groupby(['Indicator'],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,['Year'])
    
    # Configure plot
    fig = px.line(chart3_data,
                  x='Year', 
                  y='Value',
                  color='Country',
                  title='Chart 3 – Gini Index',
                  labels={'Value': 'Index Score'},# Update y-axis label
                  hover_name='Country'
                  )

    # Move legend 
    fig.update_layout(legend=dict(
       # orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05
        ))

    # Fix y-axis to zero and add margin
    fig.update_yaxes(range = [0, 100])
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Source: World Bank (for more information see data sources tab above)')

col1, col2, col3 = st.columns([1,0.05,1])

with col1:
    st.header("")
    #### Explanatory text box 4
    st.markdown("""<div style="text-align: justify;"> What the Gini Index measures can alternatively be illustrated by ranking a society by 
                its income and showing how income is allocated to <i>five</i> citizen groups of <i>equal size</i>. 
                The result of this approach is presented in chart 4. What does it say? That (in most countries) 
                the “upper 20%” of the population receives an over-proportional share of the generated income. 
                Can 20% of a society work that hard that they actually produce and should therefore gain sometimes 
                up to 50% of the total income created by that society? Consequently, can the “lowest 20%” of a society 
                work so little that their group should receive only around 5% of GNI? Chart 3 approximates what these 
                relative values are in actual annual gross income in <a href="https://en.wikipedia.org/wiki/International_dollar"> 2017 international $</a>. 
                </div>""", unsafe_allow_html=True
                ) 
with col3:
    # Get data
    chart4_data =  get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, 
                                          ['Income share held by lowest 20%',
                                           'Income share held by fourth 20%',
                                           'Income share held by third 20%',
                                           'Income share held by second 20%',
                                           'Income share held by highest 20%', 
                                           ])
    ### Group data by year
    chart4_data = chart4_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')

    # Configure plot
    fig = px.bar(chart4_data,
                  x="Year", 
                  y="Value",
                  color='Indicator',
                  facet_col='Country',
                  title='Chart 4 – Income shares of GNI',
                  facet_col_wrap=2,
                  hover_name="Country",
                  labels={
                      'Value':'Percentage'
                  }
                  )
    
    # Fix y-axis to always show (100%)
    fig.update_yaxes(range=[0, 100])

    # Move legend 
    fig.update_layout(legend=dict(
            #orientation="h",
            yanchor="bottom",
            y=-0.7,
            xanchor="left",
            x=-0.05
            ))

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns([1,0.05,1])
with col1:
    st.header("")
    #### Explanatory text box 4
    st.markdown("""<div style="text-align: justify;"> Let us last focus on those that have the lowest income in 
                society. Chart 5 presents the percentage of the population living from less than 2.15 <i>2017</i>
                international $ per day   (i.e., an <i>annual</i> income of 785 $ <i>after</i> taxes). 
                </div>""", unsafe_allow_html=True
                ) 
    
with col3:
    # Get data for the poverty share
    chart5_data = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Poverty Share'])
    
    ### Group data by year
    chart5_data = chart5_data.groupby([chart5_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart5_data,
                    x="Year", 
                    y="Value",   
                    color='Indicator',
                    title='Chart 5 – Share of population that lives with less than 2.15$ per person a day',
                    line_group='Country', 
                    hover_name="Country",
                    labels={
                        'Value':'Percentage'
                    }
                    )

    # Move legend 
    fig.update_layout(legend=dict(
       # orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05
        ))
    
    # Fix y-axis to zero and add margin
    fig.update_yaxes(range = [0, 100])

    # Display graph
    st.plotly_chart(fig, use_container_width=True)

    # Caption graph
    st.caption('Data Source: World Bank (for more information see data sources tab above)')

