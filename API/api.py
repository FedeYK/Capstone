from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields
from sqlalchemy.engine.row import RowMapping


ip_fede = ""
user = "root"
passw = ""
host = ""
database = "main"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

# Defining API key for authentication
api_key = "APP2023"

# Define decorator for checking API key
def require_api_key(func):
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-KEY')
        if provided_key == api_key:
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid API key'}, 401
    return wrapper

api = Api(app, version = '1.0',
    title = 'Rest Api to feed Streamlit App',
    description = """
        Rest Api to feed Streamlit App
        The API is hosted on a Google Cloud Platform App Engine instance.
        The database is hosted on a Google Cloud Platform Cloud SQL instance.
        """,
    contact = "frbarca@student.ie.edu",
    endpoint = "/api/v1"
)

# To not waste money I use this DB in my computer
# engine1 = create_engine("sqlite:///hmtest.db")
# conn = engine1.connect()

# def connect():
#      return engine1.connect()

# Connect to the database
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

# Disconnect from the database
def disconnect(conn):
    conn.close()

# Create a namespace for customers
customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)

# Create a namespace for articles
articles = Namespace('articles',
    description = 'All operations related to articles',
    path='/api/v1')
api.add_namespace(articles)

# Create a namespace for transactions
transactions = Namespace('transactions',
    description = 'All operations related to transactions',
    path='/api/v1')
api.add_namespace(transactions)

# Create a namespace for testing
testing = Namespace('testing',
    description = 'All operations related to transactions',
    path='/api/v1/test')
api.add_namespace(testing)

# Just a test to se if it works
@testing.route("/tables")
class get_all_tables(Resource):
    # @require_api_key
    def get(self):
        conn = connect()
        select = text("""SHOW TABLES;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        for row in result:
            print(row)
        return jsonify({'result': [dict(row) for row in result]})
            
#################################################################################################

#                                   CUSTOMERS

#################################################################################################

# Get all customers (Limited)
@customers.route("/customers")
class get_all_users(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = text("""
            SELECT *
            FROM customers
            LIMIT 100000;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
# Get specific customer with it's ID
@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):
    @require_api_key
    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = text("""
            SELECT *
            FROM customers
            WHERE customer_id = '{0}';""".format(id))
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    

@customers.route("/ages")
class get_ages(Resource):
     @require_api_key
     def get(self):
        conn = connect()
        select = text("""SELECT DISTINCT AGE AS age
                        FROM customers
                        ORDER BY age DESC;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/ages/<string:age1>/<string:age2>")
class get_ages(Resource):
     @require_api_key
     def get(self, age1, age2):
        age1 = str(age1)
        age2 = str(age2)
        conn = connect()
        select = text("""
                        SELECT *
                        FROM customers
                        WHERE AGE BETWEEN {0} AND {1}
                        LIMIT 100000
                        ;""".format(age1,
        age2))
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
     

# Function to convert rows to dictionaries
# Tried it because it wasn't working directly.
# It was a libraries problem
def to_dict(row):
    """
    This function will convert rows or lists of rows to dictionaries of list of
    dictionaries respectively
    """
    if type(row) == RowMapping:
        return dict(row)
    elif type(row) == list:
        return [dict(row) for row in row]

#################################################################################################

#                                   ARTICLES

#################################################################################################

# Get all articles (Limited)
@articles.route("/articles")
class get_all_articles(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = text("""
            SELECT *
            FROM articles
            ;""")
            #LIMIT 10;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        # for row in result:
        #     print(row)
        return jsonify({'result': [dict(row) for row in result]})
    
# Get distinct articles (Limited)
@articles.route("/articles/distinct")
class get_distinct_products(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = text("""SELECT DISTINCT product_group_name as prod FROM articles;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        # print("pelotudo")
        # for row in result:
        #     print(row)
        return jsonify({'result': [dict(row) for row in result]})

# Get specific article with it's ID    
@articles.route("/articles/<string:id>")
@articles.doc(params = {'id': 'The ID of the article'})
class select_article(Resource):
    @require_api_key
    @api.response(404, "ARTICLE not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = text("""
            SELECT *
            FROM articles
            WHERE article_id = '{0}';""".format(id))
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

#################################################################################################

#                                   TRANSACTIONS

#################################################################################################

# Get all transactions (Limited)
@transactions.route("/transactions")
class get_all_transactions(Resource):
    @require_api_key
    def get(self):
        conn = connect()
        select = text("""
            SELECT *
            FROM transactions
            LIMIT 500000;""")
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

# Get specific transaction with it's ID        
@transactions.route("/transactions/<string:id>")
@transactions.doc(params = {'id': 'The ID of the transaction'})
class select_transaction(Resource):
    @require_api_key 
    @api.response(404, "TRANSACTION not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = text("""
            SELECT *
            FROM transactions
            WHERE transaction_id = '{0}';""").format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})



    


if __name__ == '__main__':
    app.run(debug = True)