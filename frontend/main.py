from sqlalchemy import create_engine, engine, text
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from PIL import Image
import altair as alt
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import matplotlib.pyplot as plt
import plotly.express as px



# I want to check how much space does the data take
import sys

# CSS For KPI's
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Creating the login
# Authentication based on https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login('Login', 'main')

# Define the API key
headers = {'x-api-key': 'APP2023'}

# Function to load data from the database based on a query
@st.experimental_memo # @st.cache_data # Used to cache the data and make it faster
def load_data(path):
    """
    Function to load data from the api according to the path
    """
    try:
        response = requests.get(path, headers=headers)
        json_data = response.json()
        data = pd.DataFrame(json_data['result'])
    except Exception as e:
        print(e)
    return data 


# The IP where the Rest Api is running
ip = "https://api-dot-capstone-376415.oa.r.appspot.com"
# ip = "http://127.0.0.1:5000"



# From here on, we are going to use the Streamlit library to create a dashboard
# All this is already what will be displayed on the streamlit web application


if authentication_status:
    # Logout button
    authenticator.logout('Logout', 'main')

    # H&M Logo
    image = Image.open("HMLOGO.png")
    st.image(image, width=300 , use_column_width=False)

    # Welcome message
    st.write("""
    # Welcome to the H&M Dashboard 
    ### Here you will find all the information you need about our business
    """)

    # Start to load all the data that we will need
    # Creation of filters to then filter and mix the data

    # Loads the ages that we have in customers DB.
    age_path = ip + "/api/v1/ages"
    age_df = load_data(age_path)

    # Makes a lists with the ages for the filters
    age_lst = age_df["age"].to_list()
    # Trying to free space to make the app faster
    del age_df

    # Gives the sidebar a title
    st.sidebar.write("# FILTERS")

    # Creates a slider with the ages in age_lst. As default ages from 20 to 45 are selected
    age_filtered_lst = st.sidebar.slider(
        'Select a range of ages',
        0, 100, (20, 45))

    # Loads the customers DB with the filtered ages
    c_path = ip + f"/api/v1/ages/{age_filtered_lst[0]}/{age_filtered_lst[1]}"
    customer_df = load_data(c_path)

    # Let's start with the transactions DB
    # Load full transaction DB (Or what is limited in the API)
    t_path = ip + "/api/v1/transactions"
    transactions_df = load_data(t_path)

    # Join it with the customers to filter by age
    transactions_df = transactions_df.merge(customer_df, on="customer_id")

    # Online or in store filter
    st.sidebar.write("# Select sales channel")
    sales_flt_list = st.sidebar.selectbox(
        label="Select sales channel",
        options=["All", "Online", "In store" ]
    )

    # Filter according to the channel selected and create the future title
    if "All" in sales_flt_list: 
        title = "## Total amount sold by date"
        trans_filt = transactions_df
    elif "Online" in sales_flt_list:
        title = "## Total Online amount sold by date"
        trans_filt = transactions_df[transactions_df["sales_channel_id"] == 1]
    elif "In store" in sales_flt_list:
        title = "## Total In Store amount sold by date"
        trans_filt = transactions_df[transactions_df["sales_channel_id"] == 2]

    # Let's try with some Articles
    # Load list of products
    a_path = ip + "/api/v1/articles/distinct"
    articles_prod_df = load_data(a_path)
    articles_prod_df = articles_prod_df['prod'].to_list()
    articles_prod_df.insert(0, "All Products")

    # Display the product filter
    st.sidebar.write("# Select Product Type")
    sales_flt_list = st.sidebar.multiselect(
        label="Product Type",
        options=articles_prod_df,
        default="All Products")

    # Load the articles df
    a_path = ip + "/api/v1/articles"
    articles_df = load_data(a_path)

    # sales_list = sales_flt_list.tolist()
    joined_prod_trans = pd.merge(articles_df, trans_filt, on='article_id', how='inner')

    # Filter the DataFrame to include only the products in sales_flt_list
    if "All Products" not in sales_flt_list:
        joined_prod_trans = joined_prod_trans[joined_prod_trans["product_group_name"].isin(sales_flt_list)]#.sort_values("Total Sales (€)", ascending=False)

    # Club member status
    club_status = customer_df["club_member_status"].unique()
    club_status = np.insert(club_status, 0, "All Statuses")
    st.sidebar.write("# Select club member status")
    club_flt_list = st.sidebar.multiselect(
        label="Club member status",
        options=club_status,
        default="All Statuses")

    # Filter the DataFrame to include only the products in club_flt_list
    if "All Statuses" not in club_flt_list:
        joined_prod_trans = joined_prod_trans[joined_prod_trans["club_member_status"].isin(club_flt_list)]
        dochart = False
    else:
        dochart = True

    # Recieve advertising ?
    adv_status = customer_df["fashion_news_frequency"].unique()
    adv_status = np.insert(adv_status, 0, "All Frequencies")
    st.sidebar.write("# Select fashion news frequency")
    adv_flt_list = st.sidebar.multiselect(
        label="Fashion news frequency",
        options=adv_status,
        default="All Frequencies")
    
    # Filter the DataFrame to include only the products in adv_flt_list
    if "All Frequencies" not in adv_flt_list:
        joined_prod_trans = joined_prod_trans[joined_prod_trans["fashion_news_frequency"].isin(adv_flt_list)]
        dochart1 = False
    else:
        dochart1 = True


    #############################################################################################################################
    # Title
    st.write("## Total number of customers by age")

    # Count the number of customers for the selected filters
    num_customers = len(joined_prod_trans["customer_id"].unique())#.unique()

    # Calculate the average age for the selected filters
    avg_age = np.mean(joined_prod_trans["age"])

    # Create the KPI's columns & metrics
    kpi1, kpi2 = st.columns(2)

    kpi1.metric(
        label = "Number of different customers",
        value = num_customers,
        # delta = num_customers,
    )
            
    kpi2.metric(
        label = "Average age of customers",
        value = round(avg_age, 2),
        # delta = -10 + avg_age,
    )

    # Plots a bar chart with the number of customers per age
    st.bar_chart(joined_prod_trans.groupby(["age"])["customer_id"].count())

    # Title for this KPI's
    st.write("## Transactions useful information")
    # KPI's
    kpi1, kpi2, kpi3 = st.columns(3)

    # KPI 1 - Number of transactions
    num_transactions = len(joined_prod_trans)
    kpi1.metric(
        label = "Total transactions",
        value = num_transactions,
    )

    # KPI 2 - Number of transactions online
    num_transactions_online = len(joined_prod_trans[joined_prod_trans["sales_channel_id"] == 1])
    kpi2.metric(
        label = "N° of online transactions",
        value = num_transactions_online,
    )

    # KPI 3 - Number of transactions in store
    num_transactions_store = len(joined_prod_trans[joined_prod_trans["sales_channel_id"] == 2])
    kpi3.metric(
        label = "N° of in store transactions",
        value = num_transactions_store,
    )

    kpi4, kpi5, kpi6 = st.columns(3)

    # KPI 4 - Amount sold total
    amount_sold_total = joined_prod_trans["price"].sum()
    kpi4.metric(
        label = "Total amount sold in €",
        value = round(amount_sold_total, 2),
    )

    # KPI 5 - Amount sold online
    amount_sold_online = joined_prod_trans[joined_prod_trans["sales_channel_id"] == 1]["price"].sum()
    kpi5.metric(
        label = "Total amount sold online in €",
        value = round(amount_sold_online, 2),
    )

    # KPI 6 - Amount sold in store
    amount_sold_store = joined_prod_trans[joined_prod_trans["sales_channel_id"] == 2]["price"].sum()
    kpi6.metric(
        label = "Total amount sold in store in €",
        value = round(amount_sold_store, 2),
    )

    # Sales per day chart
    st.write("## Total sales per day")
    st.bar_chart(joined_prod_trans.groupby(["t_dat"])["price"].sum())

    # Going to display the total sales by product type
    ammount = joined_prod_trans.groupby(["product_group_name"])["price"].sum().round(2)

    # Create a new DataFrame from the ammount dictionary
    df = pd.DataFrame({"Product Name": ammount.index, "Total Sales (€)": ammount.values})
    # Free up memory
    del ammount
    # del joined_prod_trans

    # Filter the DataFrame to include only the products in sales_flt_list
    if "All Products" in sales_flt_list:
        df = df.sort_values("Total Sales (€)", ascending=False)
    else:    
        df = df[df["Product Name"].isin(sales_flt_list)].sort_values("Total Sales (€)", ascending=False)

    st.write("## Total sales by product type")

    # Display the DataFrame as a table in Streamlit
    st.table(df[['Product Name', 'Total Sales (€)']])

    # Bar chart of the cuantity of sales per color
    st.write("## Total sales by color")
    # st.bar_chart(joined_prod_trans.groupby(["colour_group_name"])["sales_channel_id"].count())

    # Bar chart of the cuantity of sales per color
    # Group the data by colour_group_name and count the sales_channel_id
    color_counts = joined_prod_trans.groupby("colour_group_name")["sales_channel_id"].count().reset_index()

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(color_counts["colour_group_name"], color_counts["sales_channel_id"])
    ax.set_xlabel("Color")
    ax.set_ylabel("Number of Sales")
    ax.set_xticklabels(color_counts["colour_group_name"], fontsize=8, rotation=90)
    ax.set_yscale("function", functions=(lambda x: x**0.5, lambda x: x**2))

    # Display the chart using Streamlit
    st.pyplot(fig)
    
    # Pie chart of the distribution of Club Member Status
    if dochart:
        # Create a pie chart using Altair
        st.write("## Club Member Status")
        subscriptions = joined_prod_trans['club_member_status'].value_counts()
        chart_data = pd.DataFrame({
            'count': subscriptions.values,
            'status': subscriptions.index
        })
        fig = px.pie(chart_data, values='count', names='status')
        st.plotly_chart(fig, use_container_width=True)


        # club_member_counts = joined_prod_trans['club_member_status'].value_counts()
        # chart_data = pd.DataFrame({
        #     'count': club_member_counts.values,
        #     'status': club_member_counts.index
        # })
        # chart = alt.Chart(chart_data).mark_arc().encode(
        #     theta='count',
        #     color='status'
        # )
        # st.altair_chart(chart, use_container_width=True)
    
        st.write("### Club Member Status in numbers")
        st.dataframe(chart_data)

    if dochart1:
        # Pie chart of the Newsletter Subscription Status
        st.write("## Newsletter Subscription Status")
        subscriptions = joined_prod_trans['fashion_news_frequency'].value_counts()
        chart_data = pd.DataFrame({
            'count': subscriptions.values,
            'status': subscriptions.index
        })
        fig = px.pie(chart_data, values='count', names='status')
        st.plotly_chart(fig, use_container_width=True)

        st.write("### Newsletter Subscription Status in numbers")
        st.dataframe(chart_data)

        

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')