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
df_employ = load_data("data/employment_data.xlsx")

# Get a country, region and indicator list
df_countries = df_employ['Country'].unique().tolist()
df_indicators = df_employ['Indicator'].unique().tolist()
df_regions = df_employ['Region'].unique().tolist()
df_subregion = df_employ['Sub-region'].unique().tolist()
df_sub_region = df_regions + df_subregion

# Turn years into int (str necessary first because Streamlit)
df_employ['Year'] = df_employ['Year'].astype(str)
df_employ['Year'] = df_employ['Year'].astype(int)

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
    df_fltr = df_employ[(df_employ['Country'].isin(country_selec)) & 
                       (df_employ['Year'] >= start_year_selec) & 
                       (df_employ['Indicator'].isin(indicator_selec)) &
                       (df_employ['Year'] <= end_year_selec)]
    
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
    start_year_country = int(df_employ[df_employ['Country'] == country_input]['Year'].min())
    end_year_country = int(df_employ[df_employ['Country'] == country_input]['Year'].max())

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

csv = convert_df(df_employ)

# Add empty space to create some distance 
st.sidebar.header("")

st.sidebar.download_button(label="Download full data as csv file",
                   data=csv, 
                   file_name='employment_data.csv')

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
st.title("Employment Indicators")
st.write("""
        This dashboard provides a holistic 
        overview of the economic situation in different countries, using the most important 
        macroeconomic indicators for employment. The data displayed 
        is derived from reputable international organizations. More information can be found 
        in the data sources tab below. This interactive platform allows users to get a quick 
        overview of the current employment situation in different 
        countries while taking a gender perspective and allowing for comparison with peer countries. 
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
        """,unsafe_allow_html=True)
    
############################# ROW 1 ###################################

st.header("")

# Display subheading 
st.subheader(f"Who is working in the economy in {selected_country}?")

# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

### GRAPH AND TEXT 1 ###

with col1: 

    # Create distance
    st.header("")

    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">All the goods and services an economy creates are formed 
                by three different factors of production: <strong>land</strong>, <strong>capital</strong>, and 
                <strong>labour</strong>. Let us take a closer look at 
                the latter: Who is working in an economy?</div> 
                <br>
                <div style="text-align: justify;">Naturally, the population of a country 
                can be thought of as a starting point. However, children must not work. Hence, 
                the working-age population is the population above the legal working age. Although 
                the legal working age might be higher, the ILO sets the minimum working age for 
                statistical purposes at 15 years. You can see the corresponding ILO <em>estimates</em> of 
                the working age population in chart 1. The gap to the population line is consequently 
                the number of children or rather those under 15 years in the country of interest.</div>""", unsafe_allow_html=True
    )
    
    #st.header("")

    #### Graph 1

with col3: 

    # Get data
    chart1_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, ['Population', 'Population in working age', 'Labour force', 'Employment'])
    
    ### Group data by year
    chart1_data = chart1_data.groupby([chart1_data.Indicator],group_keys=False,sort=False).apply(pd.DataFrame.sort_values,'Year')
    
    # Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value", 
                    color='Indicator',
                    hover_name="Value",
                    #title='Chart 1 - Employment and labour force as a share of the population',
                    labels={
                     "Value": "Number of people",
                 }
                    )
     
    # Legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="left",
        x=-0.05,
        ))
    
    # Set yaxis to zero
    #fig.update_yaxes(rangemode="tozero")

    # Fix y-axis to zero and add margin
    fig.update_yaxes(range = [0, ((max(chart1_data.Value))*1.2)])
    
    #Title 
    st.header("")
    st.markdown(f"""<div style="text-align: justify;"><b>Chart 1 - Employment 
                and labour force as a share of the population</div></b>""", unsafe_allow_html=True)


    # Display graph
    st.plotly_chart(fig, use_container_width=True)
    
    # Caption graph
    st.caption('Data Sources: World Bank, ILO (for more information see data sources tab above)')

# Create distance
st.header("")


############################# ROW 2 ###################################

# Subheader 
st.subheader("Who is being paid for work?")

### GRAPH AND TEXT 2 ###
# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

with col1: 

    st.header("")

    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">Next, let us ask who among those persons in working age is paid for work. For instance, 
                household work (which is worldwide predominantly performed by women) such as cleaning and cooking, 
                or childcare and caring for elderly are all not being paid. Also, be aware that subsistence farmers 
                who mainly produce for their own consumption and not for the market do not gain income. In this sense, 
                all those persons who are engaged in any activity to produce for pay or profit are understood as being 
                employed. In turn, all those persons who are without such an engagement but are available and search 
                for it are considered as unemployed. The sum of the persons employed and unemployed is called labour 
                force. Consequently, if you subtract employment from the labour force you get unemployment.</div> 
                <br>
                <div style="text-align: justify;">The indicators in chart 1 can be set closer into relation. For instance, if you divide the 
                working age population by the labour force you get the labour force participation rate. The 
                same way, the unemployment rate is calculated: Divide the working age population by unemployment. 
                Both rates are shown in chart 2.</div>""", unsafe_allow_html=True
        )
    st.header("")    

#### Graph 2

with col3:

    # Get data for country and for comparison chosen
    chart2_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, ['Labour force participation rate', 'Unemployment rate'])
    chart2_data_unemp = get_filtered_data([selected_country]  + selected_peer, selected_start_year, selected_end_year, ['Unemployment rate'])
    chart2_data_lf = get_filtered_data([selected_country] + selected_peer, selected_start_year, selected_end_year, ['Labour force participation rate'])
    
    #  Graphs
    tab1, tab2, tab3 = st.tabs([selected_country, "Unemployment Comparison", "Labour Force Comparison"])

    with tab1:
      
        # Configure plot
        fig = px.line(chart2_data,
                        x="Year", 
                        y="Value", 
                        color='Indicator',
                        #title ="Chart 2 - Unemployment and labour force participation rate",
                        hover_name="Value",
                        labels={
                        "Value": "Percentage",
                    }
                        )
        
        # Fix y-axis to always show (100%)
        fig.update_yaxes(range=[0, 100])

        # Move legend 
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="left",
            x=-0.05
            ))

        # Title
        st.markdown(f"""<div style="text-align: justify;"><b>Chart 2 - Unemployment 
                    and labour force participation rate in {selected_country}</div></b>""", unsafe_allow_html=True)

        # Display graph
        st.plotly_chart(fig, use_container_width=True)

        # Caption graph
        st.caption('Data Source: ILO (for more information see data sources tab above)')

        # Subtitle
        #st.markdown(f"""<div style="text-align: justify;"><em>Chart 2 - Unemployment and labour force 
         #           participation rate in {selected_country} (Data Source: ILOSTAT)</div></em>""", unsafe_allow_html=True)
        st.header("")

    
    with tab2: 

        # If the peer selection is empty show error message
        if not selected_peer: 
            st.error("Please choose one or several comparison countries.")
        
        # if peer selection chosen display graph
        else:

            # Configure plot
            fig = px.line(chart2_data_unemp,
                            x="Year", 
                            y="Value", 
                            color='Country',
                            #title="Chart 2.1 - Comparison of unemployment rates across the selected countries",
                            hover_name="Value",
                            labels={
                            "Value": "Percentage"
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
            fig.update_yaxes(range = [0, ((max(chart2_data_unemp.Value))*1.2)])

            # Title
            st.markdown(f"""<div style="text-align: justify;"><b>Chart 2.1 - Comparison 
                        of unemployment rates across the selected countries</div></b>""", unsafe_allow_html=True)

            # Display graph
            st.plotly_chart(fig, use_container_width=True)

             # Caption graph
            st.caption('Data Source: ILO (for more information see data sources tab above)')
            
            st.header("")
    
    with tab3: 
        
        # If the peer selection is empty show error message
        if not selected_peer: 
            st.error("Please choose one or several countries in the sidebar.")
        
        # if peer selection chosen display graph
        else:
          
            # Configure plot
            fig = px.line(chart2_data_lf,
                            x="Year", 
                            y="Value", 
                            color='Country',
                            #title="Chart 2.2 - Comparison of labour force rates across the selected countries",
                            hover_name="Value",
                            labels={
                            "Value": "Percentage"
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
            fig.update_yaxes(range = [0, ((max(chart2_data_lf.Value))*1.2)])
            
            # Title
            st.markdown(f"""<div style="text-align: justify;"><b>Chart 2.2 - 
                        Comparison of labour force rates across the selected countries</div></b>""", unsafe_allow_html=True)


            # Display graph
            st.plotly_chart(fig, use_container_width=True)

    
             # Caption graph
            st.caption('Data Source: ILO (for more information see data sources tab above)')
            
            st.header("")



############################# ROW 2 ###################################


### TABLE AND TEXT 2 ###

st.subheader(f"What's the women's share in {selected_country}?")

# Configure columns
col1, col2, col3 = st.columns([0.9,0.05,1])

#with col1: 
 
st.markdown(f"""<div style="text-align: justify;">Additionally, the indicators can be broken down by sex.  
            Table 1 shows for a given year for all indicators the total 
            number of persons, the number of women within each group, and 
            lastly their relative share. The table below shows the data for 
            <span style="color: red;">{selected_country}</span>
            for the year <span style="color: red;">{selected_end_year}</span>. </div>
            """, unsafe_allow_html=True
)
    
st.header("")    

    #### (3) Table 1

table1_indicators = ['Population', 
                    'Population in working age',
                    'Labour force',
                    'Employment',
                    'Youth unemployment', 
                    'Population, female share', 
                    'Population in working age, female share',
                    'Labour force, female share',
                    'Employment, female share',
                    'Youth unemployment, female share']

table1_data = get_filtered_data(selected_country, selected_end_year, selected_end_year, table1_indicators)

# Try whether the data for the given year is available
try: 
    # Create the table 
    indicator_values = {}
    for ind in table1_indicators:

        # Retrieve the values
        indicator_values[ind] = round(table1_data[table1_data['Indicator'] == ind].values[0][5])

    # Create table
    table1_dict = {
        'Indicator': ['Population', 'Working age population', 'Labour force', 'Employment', 'Youth unemployment'],
        'Total': [indicator_values[ind] for ind in table1_indicators[:5]],
        'Women': [indicator_values[ind] for ind in table1_indicators[5:]]}

    table1 = pd.DataFrame(table1_dict).reset_index(drop=True)
    table1.set_index('Indicator', inplace=True)

    # Add women's share column and round to two digits
    table1["Women's share (%)"] = round(table1['Women'] / table1['Total'].apply(lambda x: round(x / 100)),2)
    table1["Women's share (%)"] = table1["Women's share (%)"].apply(lambda x: format(x,".2f" ))

    #add commas 
    table1['Total'] = table1["Total"].apply(lambda x: format (x, ',d'))
    table1['Women'] = table1["Women"].apply(lambda x: format (x, ',d'))

    # Round to millions 
    #table1["Total (Million)"] = table1["Total (Million)"].apply(lambda x: x/1000000).apply(lambda x: round(x,2)).apply(lambda x: format(x,".2f" ))
    #table1["Women (Million)"] = table1["Women (Million)"].apply(lambda x: x/1000000).apply(lambda x: round(x,2)).apply(lambda x: format(x,".2f" ))

    # Display table

    # Title
    st.markdown(f"""<div style="text-align: justify;"><b>Table 1 - Women's share</div></b>""", unsafe_allow_html=True)
    st.header("")
    
    st.table(table1)

    st.caption("Data Sources: World Bank, ILO (for more information see data sources tab above)")

except ValueError: 
    st.error("Data for this year is not available. Try adjusting the selection on the side.")

#st.table(chart1_data)
# Create distance
st.header("")


############################# ROW 4 ###################################

### TABLE AND TEXT 2 ###

#with col1: 
st.subheader("Where do people work?")

st.markdown(f"""<div style="text-align: justify;">Let us take a closer look at those 
            persons who are employed: In which sectors do they work? Table 2 provides 
            a listing for the sectors Agriculture, Forestry and Fishing (primary sector), 
            Industry (secondary sector), and services (tertiary sector). The two latter 
            sectors are again broken down by further sub-sectors following the 
            <a href="https://unstats.un.org/unsd/publication/seriesm/seriesm_4rev4e.pdf">2008 
            International Standard Industrial Classification (ISIC, revision 4)</a>. 
            For comparison, the table also provides information what share of GDP is 
            created in which sector. Note that due to statistical reasons these GDP shares 
            often do not sum up to 100%.</div>
            <br>
            <div style="text-align: justify;">When comparing the sectoral GDP shares and 
            sectoral employment shares, for low-income countries you will often observe 
            that while a large share of employment takes place in the primary sector only 
            a relatively small amount of value is produced in that sector. This is one 
            explanation why in low income countries there is such high income inequality: 
            A large share of the labour force is working in a sector where little value and 
            thus little income is generated – while, comparing to high-income countries, a 
            relatively small proportion of the labour force is working in the tertiary sector 
            where usually considerably more value is created. The table below shows the data for 
            <span style="color: red;">{selected_country}</span>
            for the year <span style="color: red;">{selected_end_year}</span>.</div>
            """, unsafe_allow_html=True
)

st.header("")    


#### Table 2

table2_featureMap = {'Employment Agriculture; forestry and fishing': 'Primary',
                    'Employment Mining and quarrying': 'Primary',
                    'Employment Manufacturing': 'Secondary',
                    'Employment Electricity; gas; steam and air conditioning supply': 'Secondary',
                    'Employment Water supply; sewerage, waste management and remediation activities': 'Secondary',
                    'Employment Construction': 'Secondary',
                    'Employment Wholesale and retail trade; repair of motor vehicles and motorcycles': 'Tertiary', 
                    'Employment Transportation and storage': 'Tertiary',
                    'Employment Accomodation and food service activities': 'Tertiary',
                    'Employment Information and communication': 'Tertiary',
                    'Employment Financial and insurance activities': 'Tertiary',
                    'Employment Real estate activities': 'Tertiary',
                    'Employment Professional, scientific and technical activities': 'Tertiary',
                    'Employment Administrative and support service activities': 'Tertiary',
                    'Employment Public administration and defence; compulsory social security': 'Tertiary',
                    'Employment Education': 'Tertiary',
                    'Employment Human health and social work activities': 'Tertiary',
                    'Employment Arts, entertainment and recreation': 'Tertiary',
                    'Employment Other service activities': 'Tertiary',
                    'Employment Activities of households as employers; undifferentiated goods- and services-producing activities of households for own use': 'Secondary',
                    'Employment Activities of extraterritorial organizations and bodies': 'Tertiary',
                    'Employment Not elsewhere classified': 'Other'
                    }             

table2_data = get_filtered_data(selected_country, selected_end_year, selected_end_year, table2_featureMap.keys())

#  Retrieve employment value for the year
employment_in_year = get_filtered_data(selected_country, selected_end_year, selected_end_year, ["Employment"]).values[0][5]

# Create the table 
indicator_values_table2 = {}

for ind in table2_featureMap.keys():

    # Retrieve the value 
    employ_value = table2_data[table2_data['Indicator'] == ind].values[0][5]

    # Assign value
    #indicator_values_table2[ind] = format(round((employ_value / employment_in_year) *100,2),".2f")
    indicator_values_table2[ind] = round((employ_value / employment_in_year) *100,2)

table2_dict = {
    'Sub Sector': indicator_values_table2.keys(),
    'Employment Share (%)': indicator_values_table2.values()}

table2 = pd.DataFrame(table2_dict).reset_index(drop=True)

# Add sector column
table2["Sector"] = table2['Sub Sector'].map(table2_featureMap)

# Take out employment 
table2["Sub Sector"] = table2["Sub Sector"].apply(lambda x: x[11:])

# Reorder columns
table2 = table2[['Sector', 'Sub Sector', 'Employment Share (%)']]

# Drop old other column and add new other so that percentages add up to 100% 
table2 = table2[table2['Sub Sector'] != 'Other service activities']
sum_columns = table2['Employment Share (%)'].apply(lambda x: float(x)).sum()
missing_value = 100 - sum_columns
missing_value = round(missing_value,2)
new_row = pd.DataFrame({'Sector': ['Other'],
                         'Sub Sector': ['Other'],
                         'Employment Share (%)': [missing_value]})
# Append the new row to the DataFrame
table2 = table2.append(new_row, ignore_index=True)

# Combine both "Other" columns 
rows_to_combine = table2[(table2['Sector'] == 'Other') | (table2['Sub Sector'] == 'Not elsewhere classified')]
combined_value = rows_to_combine['Employment Share (%)'].sum()
new_row = pd.DataFrame({'Employment Share (%)': [combined_value], 'Sub Sector': 'Other', 'Sector': 'Other'})
table2 = table2.append(new_row, ignore_index=True)
table2 = table2.drop(rows_to_combine.index)


# Sort the values
table2['Employment Share (%)'] = table2['Employment Share (%)'].astype(float)
order = ['Primary', 'Secondary', 'Tertiary', 'Other']
table2['Sector'] = pd.Categorical(table2['Sector'], categories=order, ordered=True)
table2 = table2.sort_values('Sector')
table2 = table2.sort_values(by=['Sector', 'Employment Share (%)'], ascending=[True, False])
table2 = table2.reset_index(drop=True)
table2['Employment Share (%)'] = [f'{value:.2f}' for value in table2['Employment Share (%)']]


# Check if data available
if sum(table2['Employment Share (%)'] == 'nan') < (len(table2['Employment Share (%)']) /2): 

    # Title 
    st.markdown(f"""<div style="text-align: justify;"><b>Table 2 - Employment share across different subsectors</div></b>""", unsafe_allow_html=True)
    st.header("")

    # Display table
    st.table(table2.set_index("Sub Sector"))

    # Subtitle
    #st.markdown(f"""<div style="text-align: justify;"><em>Table 2 - Employment share across different subsectors (Data Source: ILOSTAT)</div></em>""", unsafe_allow_html=True)
    #st.header("")

    # Caption graph
    st.caption('Data Source: ILO (for more information see data sources tab above)')

    ###### CHARTS

    # Set title 
    #st.subheader("Employment and GDP Share per Sector")

    # Configure columns
    col1, col2, col3 = st.columns([1,0.05,1])

    # Pie Chart
    with col1:

        # Explanatory text
        st.markdown(f"""<div style="text-align: justify;">As a graphical representation of the table above, 
                    the pie chart below provides a visual overview of employment shares across the different 
                    subsectors. To see the aggregated shares of employment for the primary, secondary and 
                    tertiary sector, please click on the toggle below. A remaining percentage share of employment
                    has not been classified. This can be seen in the graph under the category "Other".</div>""", unsafe_allow_html=True)
        
        # Title
        st.subheader("")
        st.markdown(f"""<div style="text-align: justify;"><b>Chart 3 - Employment shares 
                    for {selected_country} in {selected_end_year}</div></b>""", unsafe_allow_html=True)
        st.subheader("")

        # Toggle
        on = st.toggle('Show aggregates')

        # Get disaggregated data
        table2['Employment Share (%)'] = table2['Employment Share (%)'].astype(float)
        table2.loc[table2['Employment Share (%)'] < 4, 'Sub Sector'] = 'Other Sectors' # Represent only large countries

        # Get aggregated data
        table2_agg = table2
        table2_agg['Employment Share (%)'] = table2_agg['Employment Share (%)'].astype(float)
        table2_agg = table2_agg.groupby("Sector")["Employment Share (%)"].sum()
        table2_agg = table2_agg.reset_index()

        # If the toggle is activated 
        if on:
          
            # Display aggregate pie chart 
            fig_2 = px.pie(table2_agg,
                            values="Employment Share (%)",
                            #title=f"Aggregated employment shares for {selected_country} in {selected_end_year}",
                            names="Sector")
                        
            fig_2.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig_2.update(layout_showlegend=False)
            fig_2.update_traces(textposition='inside', textinfo='percent+label')
            
            # Display graph
            st.plotly_chart(fig_2, use_container_width=True)

            # Subtitle
            #st.subheader("")
            #st.markdown(f"""<div style="text-align: justify;"><em>Chart 3 - Employment share across the three main sectors (Data Source: ILOSTAT)</div></em>""", unsafe_allow_html=True)
            st.caption("(Data Source: ILO (for more information see data sources tab above)")    
        
        # If toggle not activated
        else:

            # Configure detailed pie chart
            fig_2 = px.pie(table2,
                        values="Employment Share (%)",
                        #title=f"Employment shares across different subsectors for {selected_country} in {selected_end_year}",
                        names="Sub Sector")
            
            fig_2.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig_2.update(layout_showlegend=False)
            fig_2.update_traces(textposition='inside', textinfo='percent+label')
            
            # Display graph
            st.plotly_chart(fig_2, use_container_width=True)

            # Subtitle
            #st.subheader("")
            #st.markdown(f"""<div style="text-align: justify;"><em>Chart 3 - Employment share across different subsectors (Data Source: ILOSTAT)</div></em>""", unsafe_allow_html=True)
            st.caption("Data Source: ILO (for more information see data sources tab above)")


    ### BAR CHART
    
    with col3: 

        # Explanatory text
        st.markdown(f"""<div style="text-align: justify;"> To get a better picture of the productivity in the different sectors, 
                    one can see a comparison between Employment Share (%) and GDP Share (%) in the bar chart below. The chart also 
                    gives an indication of the labour- and capital-intensivity of the three different sectors.</div>""", unsafe_allow_html=True)
        
        # Title
        st.header("")
        st.header("")
        st.markdown(f"""<div style="text-align: justify;"><b> Chart 4 - Employment and GDP Shares for {selected_country} in {selected_end_year}</div></b>""", unsafe_allow_html=True)
        st.header("")
        st.header("")

        # define data 
        gdp_share_data = get_filtered_data([selected_country], selected_end_year, selected_end_year, ['GDP Share Agriculture (%)', 'GDP Share Industry (%)', 'GDP Share Services (%)'])
        bar_data = table2_agg
        bar_data.insert(2, 'GDP Share (%)', gdp_share_data['Value'])
        bar_data = bar_data[bar_data['Sector'] != 'Other']        
        bar_data_long = pd.melt(bar_data, id_vars=["Sector"], var_name="Share Type", value_name="Share")

        # Display bar chart
        fig = px.bar(bar_data_long,
                       x="Sector",
                       y="Share",
                       #title=f"Employment and GDP Shares for {selected_country} in {selected_end_year}",
                       color="Share Type",
                       barmode='group'
                       )
                                           
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        #fig.update(layout_showlegend=False)

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

        # Subtitle
        #st.subheader("")
        #st.markdown(f"""<div style="text-align: justify;"><em>Chart 4 - Employment vs GDP Share (Data Sources: WDI, ILOSTAT)</div></em>""", unsafe_allow_html=True)
        st.caption("Data Sources: World Bank, ILO (for more information see data sources tab above)")
else: 
    with col1:
        st.error("Data for this year is not available. Try adjusting the selection on the side.")