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

#df_selected = get_filtered_data("Germany", 2015, 2017, ['Total population'])
#print(df_selected)

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
    chart2_data = get_filtered_data("Germany", 2015, 2020, ['Labour force participation rate', 'Unemployment rate'])

    # Configure plot
    fig = px.line(chart2_data,
                    x="Year", 
                    y="Value", 
                    color='Indicator',
                    hover_name="Value"
                    )
    
    # Display graph
    st.plotly_chart(fig, use_container_width=True)


### TABLE AND TEXT 2 ###
# Configure columns
col1, col2, col3 = st.columns([1,0.05,1])

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
                

table2_indicators = key_list = list(table2_featureMap.keys())


table2_data = get_filtered_data("Germany", 2015, 2015, table2_indicators)

# Create the table 
indicator_values_table2 = {}
for condition in table2_indicators:
     indicator_values[condition] = table1_data[table1_data['Indicator'] == condition].values[0][5]

# table1_dict = {
#     'Indicator': ['Population', 'Working age population', 'Labour force', 'Formal employment', 'Youth unemployment'],
#     'Total (Million)': [indicator_values[condition] for condition in table1_indicators[:5]],
#     'Women (Million)': [indicator_values[condition] for condition in table1_indicators[5:]]}

# table1 = pd.DataFrame(table1_dict).reset_index(drop=True)
# table1.set_index('Indicator', inplace=True)

# # Add women's share column
# table1["Women's share (%)"] = table1['Women (Million)'] / table1['Total (Million)'].apply(lambda x: round(x / 100),2)

# # Display table
# st.table(table1)










############ OLD ############


   # Set font size 
    #st.markdown("""
    #<style>
    #.big-font {
    #    font-size:28px !important;
    #}
    #</style>
    #""", unsafe_allow_html=True)


#with col3: 
 #   st.header('Plot of Data')
  #  st.line_chart(data=df_employ[df_employ['Country or Area'] == "USA"], x="Year", y="GDP per capita in USD", )


# Map 
#df = pd.DataFrame(
 #   np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
  #  columns=['lat', 'lon'])

# st.map(df)

# # Display dataframe 
# #st.table(df_wb.iloc[0:10])
# #st.json({'foo':'bar','fu':'ba'})
# #st.metric(label="Temp", value="273 K", delta="1.2 K")

# # Create a section for the dataframe statistics
# #st.header('Statistics of Dataframe')
# #st.write(df_wb.describe())

# # Create a section for the dataframe header
# #st.header('Header of Dataframe')
# #st.write(df_wb.head())

# # Create a section for matplotlib figure
# #st.header('Plot of Data')

# # Plot graph
# #st.line_chart(data=df_wb, x="Year", y="GDP per capita in USD", )



# ######## Download data #########

# st.sidebar.title("Get the data!")


# @st.cache_data
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')

# csv_file = convert_df(df_employ)

# download_button = st.sidebar.download_button(
#    label='Download data as CSV', 
#    data=csv_file,
#    file_name='macroeconomic_indicators.csv',
#    mime='text/csv'
# )

# #if st.download_button(...):
#  #  st.sidebar.write('Thanks for downloading!')

# # Add widgets to sidebar 
# #st.sidebar.button
# #hit_me_button = st.sidebar.radio('R:',[1,2])

# # Lay out your app 
# #st.form('my_form_identifier')
# #st.form_submit_button('Submit to me')
# #st.container()
# #st.columns(spec)
# #col1, col2 = st.columns(2)
# #col1.subheader('Columnisation')
# #st.expander('Expander')
# #with st.expander('Expand'):
# #     st.write('Juicy deets')



