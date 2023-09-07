import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Use full screen 
st.set_page_config(layout="wide")

#---------------------------------- LOAD DATA AND GET PARAMETERS ---------------------------------

# Create import function with cache (cache so data is only loaded once)
@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    return df

# Load data 
df_employ = load_data("data/employment_data.xlsx")

# Get a country, region and indicator list
df_countries = df_employ['Country'].unique().tolist()
df_indicators = df_employ['Indicator'].unique().tolist()
df_regions = df_employ['Region'].unique().tolist()

# Turn years into int (str necessary first because Streamlit)
#df_employ['Year'] = pd.to_numeric(df_employ['Year'])
df_employ['Year'] = df_employ['Year'].astype(str)
df_employ['Year'] = df_employ['Year'].astype(int)

# Get start and end year from df 
START_YEAR = df_employ['Year'].min()
END_YEAR = df_employ['Year'].max()

#------------------------------ Function data selection ------------------------------

def get_filtered_data(country_selec, start_year_selec, end_year_selec, indicator_selec):

    """
    Function takes the user selection of the dashboard as an input and retrieves the
    corresponding data from the dataset. The output is a filtered dataframe. 

    """
    df_fltr = df_employ[(df_employ['Country'] == country_selec) & 
                       (df_employ['Year'] >= start_year_selec) & 
                       (df_employ['Indicator'].isin(indicator_selec)) &
                       (df_employ['Year'] <= end_year_selec)]
    return df_fltr


#---------------------------------------- SIDEBAR ---------------------------------

# Add title
add_title = st.sidebar.title("Customize your data")

# Add country selection
selected_country = st.sidebar.selectbox(
    label="Choose your country of interest",
    options=df_countries
    )

# Add peer country selection
selected_peer = st.sidebar.multiselect(
    "Choose comparison region",
    df_countries
    )

selected_region = st.sidebar.multiselect(
    "Choose comparison countries",
    df_countries
    )

selected_start_year = st.sidebar.slider(
     "Select the start year",
     min_value=2000, 
     max_value=2022
    )

selected_end_year = st.sidebar.slider(
     "Select the end year",
     min_value=2000, 
     max_value=2022
    )

# Download the full dataset 
# Create a csv version of the dataframe (cache so it doesn't rerun)
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df_employ)

# Add empty space to create some distance 
st.sidebar.header("")

st.sidebar.download_button(label="Click here to download data as csv",
                   data=csv, 
                   file_name='employment_data.xlsx')

st.sidebar.header("")

st.sidebar.info("""Please note that his dashboard is a prototype. 
                Users are advised that the tool may contain errors, 
                bugs, or limitations and should be used with caution 
                and awareness of potential risks, and the developers 
                make no warranties or guarantees regarding its performance, 
                reliability, or suitability for any specific purpose.""")


#---------------------------------------- MAIN PAGE --------------------------------------------

# Add a title and intro text
st.title("Employment Indicators")
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
    
############################# ROW 1 ###################################

# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

### GRAPH AND TEXT 1 ###

with col1: 

    # Display subheading 
    st.subheader("Who is working in the economy?")

    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">All the goods and services an economy creates are formed 
                by three different factors of production: <strong>land</strong>, <strong>capital</strong>, and 
                <strong>labour</strong>. Let us take a closer look at 
                the latter: Who is working in an economy? Naturally, the population of a country 
                can be thought of as a starting point. However, children must not work. Hence, 
                the working-age population is the population above the legal working age. Although 
                the legal working age might be higher, the ILO sets the minimum working age for 
                statistical purposes at 15 years. You can see the corresponding ILO estimates of 
                the working age population in chart 1. The gap to the population line is consequently 
                the number of children or rather those under 15 years in the country of interest.</div>""", unsafe_allow_html=True
    )
    
    #### Graph 1

with col1: 
    # Get data
    chart1_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, ['Population', 'Population in working age', 'Labour force', 'Employment'])

    # Configure plot
    fig = px.line(chart1_data,
                    x="Year", 
                    y="Value", 
                    color='Indicator',
                    hover_name="Value"
                    )
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)


### TABLE AND TEXT 2 ###

with col3: 
 
    st.subheader("What's the women's share?")

    st.markdown(f"""<div style="text-align: justify;">Additionally, the indicators can be broken down by sex.  
                Table 1 shows for a given year for all indicators the total 
                number of persons, the number of women within each group, and 
                lastly their relative share.</div>
                <br>
                <div style="text-align: justify;">The table below shows the data for 
                <span style="color: red;">{selected_country}</span>
                for the year <span style="color: red;">{selected_end_year}</span>. The choice of year depends on the end year selected in the 
                sidebar and can be adjusted by moving the slider.</div>
                """, unsafe_allow_html=True
    )
    
    st.header("")    

    #### (3) Table 1

    table1_indicators = ['Population', 
                        'Population in working age',
                        'Employment',
                        'Youth unemployment', 
                        'Labour force', 
                        'Population, female share', 
                        'Population in working age, female share',
                        'Employment, female share',
                        'Youth unemployment, female share',
                        'Labour force, female share']

    table1_data = get_filtered_data(selected_country, selected_end_year, selected_end_year, table1_indicators)

    # Create the table 
    indicator_values = {}
    for condition in table1_indicators:
        indicator_values[condition] = round(table1_data[table1_data['Indicator'] == condition].values[0][5])

    table1_dict = {
        'Indicator': ['Population', 'Working age population', 'Labour force', 'Formal employment', 'Youth unemployment'],
        'Total (Million)': [indicator_values[condition] for condition in table1_indicators[:5]],
        'Women (Million)': [indicator_values[condition] for condition in table1_indicators[5:]]}

    table1 = pd.DataFrame(table1_dict).reset_index(drop=True)
    table1.set_index('Indicator', inplace=True)

    # Add women's share column and round to two digits
    table1["Women's share (%)"] = round(table1['Women (Million)'] / table1['Total (Million)'].apply(lambda x: round(x / 100)),2)
    table1["Women's share (%)"] = table1["Women's share (%)"].apply(lambda x: format(x,".2f" ))
    table1["Women's share (%)"] = table1["Women's share (%)"]
 
    # Display table
    st.table(table1)

    
############################# ROW 2 ###################################

### GRAPH AND TEXT 2 ###
# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

with col1: 

    # Subheader 
    st.subheader("Who is being paid for their work?")


    #### Explanatory text box 1
    st.markdown("""<div style="text-align: justify;">Next, let us ask who among those persons in working age is paid for their work. For instance, 
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
       
#### Graph 2
with col3:
    # Get data
    chart2_data = get_filtered_data(selected_country, selected_start_year, selected_end_year, ['Labour force participation rate', 'Unemployment rate'])
    print(chart2_data.columns)
    # Configure plot
    fig = px.line(chart2_data,
                    x="Year", 
                    y="Value", 
                    color='Indicator',
                    hover_name="Value"
                    )
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)

############################# ROW 3 ###################################

### TABLE AND TEXT 2 ###

#with col1: 
st.subheader("Where do people work?")

st.markdown(f"""<div style="text-align: justify;">Let us take a closer look at those 
            persons who are employed: In which sectors do they work? Table 2 provides 
            a listing for the sectors Agriculture, Forestry and Fishing (primary sector), 
            Industry (secondary sector), and services (tertiary sector). The two latter 
            sectors are again broken down by further sub-sectors following the 2008 
            International Standard Industrial Classification (ISIC, revision 4). 
            For comparison, the table also provides information what share of GDP is 
            created in which sector. Note that due to statistical reasons these GDP shares 
            often do not sum up to 100%.</div>
            <br>
            <div style="text-align: justify;">When comparing the sectoral GDP shares and 
            sectoral employment shares, for developing countries you will often observe 
            that while a large share of employment takes place in the primary sector only 
            a relatively small amount of value is produced in that sector. This is one 
            explanation why in low income countries there is such high income inequality: 
            A large share of the labour force is working in a sector where little value and 
            thus little income is generated – while, comparing to high-income countries, a 
            relatively small proportion of the labour force is working in the tertiary sector 
            where usually considerably more value is created.</div>
            """, unsafe_allow_html=True
)

st.header("")    

#### Table 2
# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

with col1: 
    table2_featureMap = {'Employment Agriculture': 'Primary',
                        'Employment Mining and quarrying': 'Secondary',
                        'Employment Manufacturing': 'Secondary',
                        'Employment Utilities': 'Secondary',
                        'Employment Construct': 'Secondary',
                        'Employment Wholesale': 'Tertiary', 
                        'Employment Transport': 'Tertiary',
                        'Employment Accomodation': 'Tertiary',
                        'Employment Financial': 'Tertiary',
                        'Employment Real estate': 'Tertiary',
                        'Employment Public administration and defence': 'Tertiary',
                        'Employment Education': 'Tertiary',
                        'Employment Human health and social work activities': 'Tertiary',
                        'Employment Other services': 'Tertiary'}             

    table2_data = get_filtered_data(selected_country, selected_end_year, selected_end_year, table2_featureMap.keys())

    #  Retrieve employment value for the year
    employment_in_year = get_filtered_data(selected_country, selected_end_year, selected_end_year, ["Employment"]).values[0][5]

    # Create the table 
    indicator_values_table2 = {}

    for ind in table2_featureMap.keys():

        # Retrieve the value 
        employ_value = table2_data[table2_data['Indicator'] == ind].values[0][5]

        # Assign value
        indicator_values_table2[ind] = format(round((employ_value / employment_in_year) *100,2),".2f")

    table2_dict = {
        'Sub Sector': indicator_values_table2.keys(),
        'Employment Share (%)': indicator_values_table2.values()}

    table2 = pd.DataFrame(table2_dict).reset_index(drop=True)

    # Add sector column
    table2["Sector"] = table2['Sub Sector'].map(table2_featureMap)

    # Reorder columns
    table2 = table2[['Sector', 'Sub Sector', 'Employment Share (%)']]
    
    # Display table
    st.table(table2)

### PIE CHART 
with col3: 

    # Get data 
    table2['Employment Share (%)'] = table2['Employment Share (%)'].astype(float)
    table2.loc[table2['Employment Share (%)'] < 2, 'Sub Sector'] = 'Other Sectors' # Represent only large countries

    # Configure plot
    fig_2 = px.pie(table2,
                 values="Employment Share (%)",
                 title=f"Employment Shares for {selected_country} in {selected_end_year}",
                 names="Sub Sector")
    
    fig_2.update_layout(margin=dict(t=35, b=1, l=1, r=1))
    
    # Display graph
    st.plotly_chart(fig_2, use_container_width=True)
