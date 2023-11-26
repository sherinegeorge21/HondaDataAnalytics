

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings("ignore")

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Honda Data Dashboard", page_icon="honda.png", layout="wide")

# ---- READ EXCEL ----
df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
df1 = pd.read_csv('Alternative Fuel Vehicles US.csv')

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
make = st.sidebar.multiselect(
    "Select the Make of EVs:",
    options=df["Make"].unique(),
    default="TESLA"
)

manufacturer = st.sidebar.multiselect(
    "Select the Manufacturer of AFVs:",
    options=df1["Manufacturer"].unique(),
    default="Audi"
)

# customer_type = st.sidebar.multiselect(
#     "Select the Customer Type:",
#     options=df["Customer_type"].unique(),
#     default=df["Customer_type"].unique(),
# )

# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

df_selection = df.query(
    "Make == @make"
)

df_selection1 = df1.query(
    "Manufacturer == @manufacturer"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
# title_html = """
#     <div style="display: flex; align-items: center;">
#         <img src="honda.png" alt="Image" width="80" height="80" style="margin-right: 10px;">
#         <h1>Honda Data Analytics Case Competition</h1>
#     </div>
# """
st.image("final.jpeg",width=200, caption="")


# Render the custom title using the st.markdown function
#st.markdown(title_html, unsafe_allow_html=True)
st.title("Insights Hub - EVolutionaries")
# st.markdown("##")


def home_page():
    st.subheader("Creating a Value Proposition and Entry Strategy for a BEV Company")

    # Display an image
    st.image("band.jpg", use_column_width=True, caption="Battery Electric Vehicle")

    st.write("In a rapidly evolving automotive landscape, Battery Electric Vehicles (BEVs) are gaining prominence due to their cost savings, environmental benefits, and reduced maintenance.")

    st.write("However, as consumer preferences and values continue to diversify, companies face an increasingly complex challenge in distinguishing their offerings.")

    # Display an icon
    st.markdown(":star: **Our Task:**")
    st.markdown("""
    - We are part of a hypothetical BEV company aiming to enter the market.
    - Our challenge is to create a compelling value proposition and entry strategy.
    - Consider the following factors:
        - :chart_with_upwards_trend: **Market Analysis:** Analyze the current BEV market landscape, trends, and competitors.
        - :raising_hand: **Consumer Preferences:** Understand the diverse preferences and values of potential customers.
        - :bulb: **Product Differentiation:** Define how our BEV stands out from the competition.
        - :deciduous_tree: **Sustainability:** Highlight the environmental benefits of our BEV.
        - :world_map: **Distribution:** Plan how and where our BEV will be available.
        - :loudspeaker: **Marketing and Promotion:** Develop strategies to reach and engage the target audience.
    - Our goal is to create a comprehensive and innovative approach that sets our company apart and attracts customers.
    - Use the sidebar to navigate to other sections of this app for our analysis.
    """)

def about_page():
    # TOP KPI's
    total_sales = int(df_selection["VIN (1-10)"].count())

    average_rating = round((df_selection["Electric Range"]-df_selection["Electric Range"].min())/(df_selection["Electric Range"].max() - df_selection["Electric Range"].min()),1)
    star_rating = ":star:" * int(round(average_rating.mean(), 0))
    average_sale_by_transaction = round(df_selection["Electric Range"].mean(), 2)

    left_column,  right_column = st.columns(2)
    with left_column:
        st.subheader("Total number of vehicles produced:")
        st.subheader(f"{total_sales:,}")
    # with middle_column:
    #     st.subheader("Average Rating based on range:")
    #     st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Electric Range:")
        st.subheader(f"{average_sale_by_transaction}")

    st.markdown("""---""")

    # SALES BY PRODUCT LINE [BAR CHART]
    # sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
    # fig_product_sales = px.bar(
    #     sales_by_product_line,
    #     x="Total",
    #     y=sales_by_product_line.index,
    #     orientation="h",
    #     title="<b>Sales by Product Line</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    #     template="plotly_white",
    # )
    # fig_product_sales.update_layout(
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     xaxis=(dict(showgrid=False))
    # )

    # Filter BEVs from the alternative fuel vehicles dataset
    bevs_afv_data = df_selection1[df_selection1['Fuel'] == 'Electric']

    # # Aggregate the data to count the number of models by manufacturer
    # bevs_manufacturer_dist = bevs_afv_data['Manufacturer'].value_counts().reset_index()
    # bevs_manufacturer_dist.columns = ['Manufacturer', 'Model Count']

    # Aggregate the data to count the number of models by model year
    bevs_model_year_dist = bevs_afv_data['Model Year'].value_counts().sort_index().reset_index()
    bevs_model_year_dist.columns = ['Model Year', 'Model Count']

    # Aggregate the data to get the average electric range by vehicle type
    average_range_by_type = df_selection.groupby('Electric Vehicle Type')['Electric Range'].mean().reset_index()

    # Count the number of BEVs and PHEVs
    vehicle_type_count = df_selection['Electric Vehicle Type'].value_counts().reset_index()
    vehicle_type_count.columns = ['Electric Vehicle Type', 'Count']

    # Aggregate the data to get the average electric range by vehicle type
    average_range_by_type = df.groupby('Electric Vehicle Type')['Electric Range'].mean().reset_index()

    # Count the number of BEVs and PHEVs
    vehicle_type_count = df['Electric Vehicle Type'].value_counts().reset_index()
    vehicle_type_count.columns = ['Electric Vehicle Type', 'Count']
    top_values = 5
    fuel_type_count = df_selection1['Fuel'].value_counts().reset_index()
    fuel_type_count.columns = ['Fuel', 'Count']
    top_fuel_types = fuel_type_count.nlargest(top_values, 'Count')
    other_count = fuel_type_count['Count'].sum() - top_fuel_types['Count'].sum()

    cat_type_count = df_selection1['Category'].value_counts().reset_index()
    cat_type_count.columns = ['Category', 'CatCount']
    top_cat_types = cat_type_count.nlargest(top_values, 'CatCount')
    other_count1 = cat_type_count['CatCount'].sum() - top_cat_types['CatCount'].sum()
    #top_fuel_types = top_fuel_types.append({'Fuel': 'Others', 'Count': other_count}, ignore_index=True)
    top_cat_types=pd.concat([top_cat_types,pd.DataFrame([{'Category': 'Others', 'CatCount': other_count1}])],ignore_index=True)
    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Function to plot data
    def plot_data(df, x, y, title, xlabel, ylabel, kind="bar", rotation=0, figsize=(8,4), background_color="#f0f0f0"):
        plt.figure(figsize=figsize)
        if kind == "bar":
            sns.barplot(data=df, x=x, y=y, palette="viridis")
        elif kind == "count":
            sns.countplot(data=df, x=x, palette="viridis")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=rotation)
            # Set the background color of the plot to match the app's background
        fig = plt.gcf()
        fig.patch.set_facecolor(background_color)
        
        # Remove frame and grid lines
        sns.despine()

        st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)


    right_column,rightmost = st.columns([1, 1])

    st.subheader("Electric vehicles produced by alternate companies by Model Year:")
    # st.bar_chart(bevs_model_year_dist.set_index('Model Year'))
    # Create a Pie chart using Plotly
    fig = px.pie(
    bevs_model_year_dist, 
    values='Model Count', 
    names='Model Year', 
    #title="Electric vehicles by Model Year",
    color_discrete_sequence=px.colors.qualitative.Set3 # Choose a colorful color palette
    )
    st.plotly_chart(fig)

    # Display the pie chart using st.plotly_chart
        
    # with middle_column:
    #     st.subheader("Average Rating based on range:")
    #     st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        colors = {
        'Battery Electric Vehicle': 'blue',
        'Plug-In Hybrid Electric Vehicle': 'green'
    }
        st.subheader("Average Electric Range by Vehicle Type:")
        #st.bar_chart(average_range_by_type.set_index('Electric Vehicle Type'))
        fig = px.bar(
        average_range_by_type, 
        x='Electric Vehicle Type', 
        y='Electric Range', 
        #title="Average Electric Range by Vehicle Type",
        color='Electric Vehicle Type',  # Specify the color based on the Vehicle Type
        color_discrete_map=colors  # Use the custom color dictionary
    )

    # Display the colorful bar chart using st.plotly_chart
        st.plotly_chart(fig)

    with rightmost:
        st.subheader("Count of Electric Vehicle Types:")
        #st.bar_chart(average_range_by_type.set_index('Electric Vehicle Type'))
        colors = {
        'Battery Electric Vehicle': 'orange',
        'Plug-In Hybrid Electric Vehicle': 'purple'
    }
        #st.subheader("Average Electric Range by Vehicle Type:")
        #st.bar_chart(average_range_by_type.set_index('Electric Vehicle Type'))
        fig = px.bar(
        vehicle_type_count, 
        x='Electric Vehicle Type', 
        y='Count', 
        #title="Average Electric Range by Vehicle Type",
        color='Electric Vehicle Type',  # Specify the color based on the Vehicle Type
        color_discrete_sequence=['lightblue', 'blue'] # Use the custom color dictionary
    )
        st.plotly_chart(fig)
    st.markdown("""---""")
    st.subheader("Distribution of Alternative Fuel Types (Top 5):")
    # Define custom colors for each fuel type
    colors = ['blue', 'green', 'orange', 'red', 'purple']

    # Create a colorful pie chart using Plotly
    fig = px.pie(
        top_fuel_types, 
        values='Count', 
        names='Fuel', 
        #title="Top 5 Alternative Fuel Types",
        color_discrete_sequence=colors  # Use the custom color palette
    )

    # Display the colorful pie chart using st.plotly_chart
    st.plotly_chart(fig)

    st.markdown("""---""")
    # Plotting the distribution of vehicle types using Streamlit bar chart
    st.subheader("Distribution of Vehicle Types among Alternative Fuel Vehicles (Top 5):")
    st.bar_chart(top_cat_types.set_index('Category'))


    st.markdown("""---""")
    # Plotting the distribution of all-electric range for electric vehicles
    st.subheader("Distribution of All-Electric Range for Electric Vehicles:")
    plt.figure(figsize=(10, 6))
    bevs_afv_data['All-Electric Range'].plot(kind='hist', bins=20, color='purple')
    #plt.title('Distribution of All-Electric Range for Electric Vehicles')
    plt.xlabel('All-Electric Range (miles)')
    plt.ylabel('Number of Vehicles')
    plt.tight_layout()
    st.pyplot()

    # Counting the occurrences of each model
    model_counts = df_selection['Model'].value_counts().head(5).reset_index()
    model_counts.columns = ['Electric Vehicle Model', 'Count']  # Top 10 models

    # Bar chart for Top 10 Electric Vehicle Models using Streamlit
    st.subheader("Top 5 Electric Vehicle Models for the Make:")
    st.bar_chart(model_counts[['Electric Vehicle Model', 'Count']].set_index('Electric Vehicle Model'))

    st.markdown("""---""")
    top=10
    # Create a bar plot with custom colors
    fig, ax = plt.subplots()
    # Generate a range of colors
    mfr_type_count = df1['Manufacturer'].value_counts().reset_index()
    mfr_type_count.columns = ['Manufacturer', 'Model Count']
    top_mfr_types = mfr_type_count.nlargest(top, 'Model Count')
    other_count2 = mfr_type_count['Model Count'].sum() - mfr_type_count['Model Count'].sum()
    #top_fuel_types = top_fuel_types.append({'Fuel': 'Others', 'Count': other_count}, ignore_index=True)
    top_mfr_types=pd.concat([top_mfr_types,pd.DataFrame([{'Manufacturer': 'Others', 'Model Count': other_count2}])],ignore_index=True)
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_mfr_types))) 
    bars = ax.bar(top_mfr_types['Manufacturer'], top_mfr_types['Model Count'], color=colors)

    # Customize the plot appearance (add labels, title, etc.)
    ax.set_xlabel('Manufacturer')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title('Distribution of BEVs by Manufacturer')
    plt.xticks(rotation=90)

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Create a plot
    plt.figure(figsize=(12, 10))
    sns.countplot(x='State', data=df, palette='viridis')
    plt.xlabel('State')
    plt.ylabel('Number of Vehicles')
    plt.title(f'Number of Vehicles each state')
    plt.xticks(rotation=45)
    plt.yticks(range(0, 160000, 10000))

    # Display the plot using Streamlit
    st.pyplot(plt)

    # Create a plot
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Make', order=df['Make'].value_counts().index)
    plt.title('Vehicle Count by Make')
    plt.xticks(rotation=90)

    # Display the plot using Streamlit
    st.pyplot(plt)

        # Create a plot
    altstation=pd.read_csv("alt_fuel_stations.csv")
    plt.figure(figsize=(12, 8))
    alt_type_count = altstation['State'].value_counts().reset_index()
    alt_type_count.columns = ['State', 'Station_Count']
    sns.barplot(x='State', y='Station_Count', data=alt_type_count)
    plt.xlabel('State')
    plt.ylabel('Number of ELEC Station')
    plt.title('Distribution of ELEC Station for Each State')
    plt.xticks(rotation=45)

    # Display the plot using Streamlit
    st.pyplot(plt)

    # Create a sidebar filter for binwidth
    binwidth = st.sidebar.slider("Bin Width", min_value=1, max_value=10, value=3)

    # Create a histogram plot
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x="Model Year", hue='Clean Alternative Fuel Vehicle (CAFV) Eligibility', multiple='dodge', binwidth=binwidth)
    plt.xlabel('Model Year')
    plt.ylabel('Count')
    plt.title('Alternative Fuel Vehicle Availability by Model Year')
    plt.legend(title='CAFV Eligibility')

    # Display the plot using Streamlit
    st.pyplot(plt)





def contact_page():
    st.subheader("Meet our Team")
    left_column,  right_column,rightmost = st.columns([1,1,1])
    with left_column:
        st.image("sherine.jpg")
        st.subheader('Sherine George')

    with right_column:
        st.image("shashank.jpeg")
        st.subheader('Shashank Kallahalli Suresh')
    with rightmost:
        st.image("sherry1.png")
        st.subheader('Ming-Hsuan Li')
    
def rec_page():
     # Add images
    st.image("honda2.jpeg", use_column_width=True, caption="Honda transforming lives",width=350)
    # Section 4.1: Focus on Popular Segments
    st.subheader("Focus on Popular Segments")
    st.markdown(
        "<i class='fas fa-car'></i> Given the popularity of sedans and wagons, followed by SUVs in the alternative fuel vehicle market, prioritize these segments for new BEV models.",
        unsafe_allow_html=True,
    )

    # Section 4.2: Tesla's Prominence
    st.subheader("Tesla's Prominence")
    st.markdown(
        "<i class='fab fa-tesla'></i> Tesla, followed by Nissan, is prominent in the electric vehicle market. Consider strategies to differentiate from these market leaders, such as unique design, pricing, or technological features.",
        unsafe_allow_html=True,
    )

    # Section 4.3: CAFV Eligibility Trends
    st.subheader("CAFV Eligibility Trends")
    st.markdown(
        "<i class='fas fa-chart-line'></i> The decrease in Clean Alternative Fuel Vehicle (CAFV) eligibility over the years suggests changing regulations or consumer preferences, warranting a closer look at policy and market dynamics.",
        unsafe_allow_html=True,
    )

    # Section 4.4: Model 3's High Presence
    st.subheader("Model 3's High Presence")
    st.markdown(
        "<i class='fas fa-car'></i> The significant presence of Tesla's Model 3 suggests a strong market preference for this type of vehicle. Analyze its features and popularity to inform the development of competitive models.",
        unsafe_allow_html=True,
    )

    # Section 4.5: Diverse Fuel Options in Categories
    st.subheader("Diverse Fuel Options in Categories")
    st.markdown(
        "<i class='fas fa-gas-pump'></i> Different vehicle categories have varying alternative fuel options. This diversity indicates opportunities in niche markets with specific fuel type preferences.",
        unsafe_allow_html=True,
    )

    # Section 4.6: Geographical Focus
    st.subheader("Geographical Focus")
    st.markdown(
        "<i class='fas fa-map-marker-alt'></i> With California leading in fuel stations and Washington showing high vehicle adoption, focus on these states for initial market entry and expansion strategies.",
        unsafe_allow_html=True,
    )

    # Section 4.7: Competitive Strategy
    st.subheader("Competitive Strategy")
    st.markdown(
        "<i class='fas fa-chart-line'></i> Develop a competitive strategy that leverages Ford's focus on BEVs and other manufacturers' focus on hybrid electric vehicles, possibly exploring niche segments or innovative technology.",
        unsafe_allow_html=True,
    )

   

# Create a sidebar navigation
page = st.sidebar.selectbox("Select a Page", ["Problem Statement", "Analysis", "Recommendations","Contact"])

# Conditionally render the selected page
if page == "Problem Statement":
    home_page()
elif page == "Analysis":
    about_page()
elif page == "Contact":
    contact_page()
elif page == "Recommendations":
    rec_page()


# st.markdown("""---""")
# # Line plot for Model Year Trend Analysis using Streamlit
# st.subheader("Electric Vehicle Population by Model Year:")
# df_selection_year=df_selection[(df_selection["Model Year"]>=2017) & (df_selection["Model Year"]<=2023)]
# #st.line_chart(df_selection.set_index('Model Year'))
# st.line_chart(df.set_index('Model Year')[['2022']])




# # SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
# fig_hourly_sales = px.bar(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by hour</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )


# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
# right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
