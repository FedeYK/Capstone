# **H&M Dashboard**

The H&M Dashboard is a powerful Streamlit-based web application that provides an interactive, user-friendly interface for analyzing H&M's business data. The dashboard is designed to offer valuable insights into customer demographics, transaction details, and product information, allowing users to filter data by various attributes for a deeper understanding of sales trends and patterns.

:100:<a href='https://frontend-dot-capstone-376415.oa.r.appspot.com/'>H&M Dashboard Web Application </a>

:boom:<a href='https://api-dot-capstone-376415.oa.r.appspot.com/'>API - H&M Dashboard</a>

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/1.png" title="Dashboard Example">

## **Table of Contents**
* [Key Features](#key)
* [Prerequisites](#pre)
* [Installation](#inst)
* [Usage](#us)
* [What you get](#wyg)
* [Retail Data Api](#api)
    * [Features](#feat)
    * [Setup](#setup)
    * [Api Endpoints](#aend)
        * [Customers](#cust)
        * [Articles](#articles)
        * [Transactions](#trans)
    * [Authentication](#auth)
* [Cloud Deployment](#cloud)

## <a name='key'></a>**Key Features**

- **Secure Authentication System**: The dashboard implements an authentication mechanism to ensure only authorized users can access the data and insights.
- **Interactive Filters**: Users can easily filter the data by age range, sales channel (online or in-store), product type, and club member status to view custom insights tailored to their needs.
- **Comprehensive Key Performance Indicators (KPIs)**: The dashboard displays the following KPIs:
    - Number of unique customers
    - Average age of customers
    - Total transactions (count)
    - Number of online transactions
    - Number of in-store transactions
    - Total amount sold (in euros), including separate values for online and in-store sales
- **Data Visualizations**: The dashboard offers various visualizations to better understand the data, including:
    - Bar chart of the total number of customers by age
    - Bar chart of total sales per day
    - Table of total sales by product type, sorted by the highest-selling products
    - Bar chart of total sales by color, illustrating which colors are most popular among customers
- All this KPI’s are connected through the filters and each time a filter is changed all the KPI’s change

## <a name='pre'></a>**Prerequisites**

Before you begin, ensure you have met the following requirements:

- Python 3.7 or later
- pandas
- streamlit
- SQLAlchemy version 1.4.40
- PyMySQL
- flask
- flask-restx
- numpy
- pyyaml
- altair version 4.1.0
- streamlit-authenticator
- matplotlib
- plotly

## <a name='inst'></a>**Installation**

1. Clone this repository:

```
git clone https://github.com/FedeYK/Capstone.git
```

2. Change into the project directory:

```
cd hm-dashboard
```

3. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required libraries:

```
pip install -r requirements.txt
```

5. Configure the **`config.yaml`** file with the appropriate authentication credentials, API keys, and other required configurations.

## <a name='us'></a>**Usage**

To launch the Streamlit app, execute the following command in your terminal:

```
streamlit run app.py
```

Streamlit will then provide a local URL (e.g., **`http://localhost:8501`**) that you can use to access the dashboard in your web browser.

## <a name='wyg'></a>**What you get**

Introducing our feature-rich app that allows you to effortlessly sift through various filters such as age range, sales channels, product types, "Club Member" status, and the frequency of fashion news received by customers.

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/3.png" title="Dashboard Filters" width=300px>

Upon applying your desired filters, you'll be presented with insightful KPIs, including the total number of customers matching your criteria, their average age, and a visually appealing bar chart illustrating the distribution of customers by age.

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/4.png" title="Dashboard KPI's 1" width=300px>

Further KPIs include the total number of transactions completed, the number of online and in-store transactions, the overall revenue generated, and a breakdown of sales by channel. Additionally, you'll be greeted with a captivating bar chart displaying sales by date.

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/5.png" title="Dashboard KPI's 2" width=300px>

A comprehensive table showcases the total sales by product type based on your chosen filters, followed by an engaging bar chart highlighting sales by color.

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/6.png" title="Dashboard Ammount sold" width=300px>

Finally, our app offers two delightful pie charts that reveal the percentage of Club Members and the distribution of customers receiving fashion news according to frequency. Complementary tables provide the number of customers in each category for a thorough understanding.

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/7.png" title="Dashboard Engagement" width=300px>

Experience the seamless way to analyze your data with our aesthetically pleasing and user-friendly app.

# <a name='api'></a>**Retail Data API**

This is a RESTful API built using Flask and Flask-Restx to serve retail data for a Streamlit application. The API provides access to data related to customers, articles, and transactions. It uses Google Cloud Platform's App Engine for hosting and Cloud SQL for the database.

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/2.png" title="API Example">

## <a name='feat'></a>**Features**

- Retrieve customer data (all or by ID, age range)
- Retrieve article data (all, distinct, or by ID)
- Retrieve transaction data (all or by ID)
- API key authentication for secured access

## <a name='setup'></a>**Setup**

1. Clone this repository.
2. Install the required dependencies.

```
pip install -r requirements.txt
```

3. Set your database credentials and API key in the **`api.py`** file.

```
user = "your_user"
passw = "your_password"
host = "your_host"
database = "your_database"
api_key = "your_api_key"
```

4. Run the application.

```
bashCopy code
python app.py
```

## <a name='aend'></a>**API Endpoints**

Base URL: **`/api/v1`**

### <a name='cust'></a>**Customers**

- Get all customers: **`/api/v1/customers`**
- Get specific customer by ID: **`/api/v1/customers/<id>`**
- Get distinct ages of customers: **`/api/v1/ages`**
- Get customers between specific ages: **`/api/v1/ages/<age1>/<age2>`**

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/cust.png" title="Customers Example">

### <a name='articles'></a>**Articles**

- Get all articles: **`/api/v1/articles`**
- Get distinct articles: **`/api/v1/articles/distinct`**
- Get specific article by ID: **`/api/v1/articles/<id>`**

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/art.png" title="Articles Example">

### <a name='trans'></a>**Transactions**

- Get all transactions: **`/api/v1/transactions`**
- Get specific transaction by ID: **`/api/v1/transactions/<id>`**

<img src="https://github.com/FedeYK/Capstone/blob/main/readme/trans.png" title="Transactions Example">

## <a name='auth'></a>**Authentication**

To access the API endpoints, you need to provide an API key in the request header as **`X-API-KEY`**. The API key is defined in the **`api.py`** file.

## <a name='cloud'></a>**Cloud Deployment**

If you're contemplating deploying your app in the cloud, Google App Engine provides a seamless and sophisticated solution. Begin by creating two neatly organized folders named 'API' and 'Frontend,' then transfer the corresponding files into each folder. Rest assured, all essential files—including app.yaml, config.yaml, and requirements.txt—can be effortlessly located within these folders.

Next, venture into the Google Cloud Console and execute the command 'gcloud app deploy.' Sit back and marvel at the captivating process as your app is gracefully deployed and comes to life, ready to fulfill its purpose with elegance and efficiency.
