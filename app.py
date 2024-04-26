# Hashtags added
# Hashtags: Digitalisierung, User: tho1965, RusticusArat, String: India

from flask import Flask, render_template, request
import re
import mysql.connector
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://shubhp:Twitter123@twitter.9nanqoi.mongodb.net/Twitter?retryWrites=true&w=majority&appName=Twitter")
db = client.Twitter
tweets_collection = db.Tweets

# Connect to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Spsql@123",
  database="final"
)
mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    search_type = request.args.get('search_type')
    query = request.args.get('query')

    if search_type == 'string':
        # Search for tweets containing the query string in MongoDB
        results = tweets_collection.find({"text": {"$regex": f"(?i).*{query}.*"}}).limit(10)
        tweets = list(results)
        return render_template('search_results.html', tweets=tweets)

    elif search_type == 'user':
        # Normalize the query string
        query = re.sub(r'[^a-zA-Z0-9]', '', query)

        # Search for user in MySQL
        mycursor.execute("SELECT * FROM Users WHERE screen_name=%s", (query,))
        user = mycursor.fetchone()

        if user:
            # Search for tweets by user ID in MongoDB
            results = tweets_collection.find({"user.id_str": str(user[0])}).limit(10)
            tweets = list(results)
            return render_template('search_results.html', tweets=tweets)
        else:
            return "User not found."

    elif search_type == 'hashtag':
        # Normalize the query string
        query = re.sub(r'[^a-zA-Z0-9]', '', query)

        # Search for hashtags in MongoDB
        results = tweets_collection.find({"entities.hashtags.text": {"$regex": f"(?i)^{query}"}}).limit(10)
        tweets = list(results)
        return render_template('search_results.html', tweets=tweets)

    else:
        return "Invalid search type."

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request
# from pymongo import MongoClient
# import mysql.connector
# import re
# from flask_caching import Cache

# app = Flask(__name__)

# # Cache configuration
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://shubhp:Twitter123@twitter.9nanqoi.mongodb.net/Twitter?retryWrites=true&w=majority&appName=Twitter")
# db = client.Twitter
# tweets_collection = db.Tweets

# # Connect to MySQL
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Spsql@123",
#   database="final"
# )
# mycursor = mydb.cursor()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @cache.cached(timeout=300, key_prefix='search_results')
# @app.route('/search')
# def search():
#     search_type = request.args.get('search_type')
#     query = request.args.get('query')

#     if search_type == 'string':
#         results = tweets_collection.find({"text": {"$regex": f"(?i).*{query}.*"}}).limit(10)
#         tweets = list(results)
#         return render_template('search_results.html', tweets=tweets)

#     elif search_type == 'user':
#         query = re.sub(r'[^a-zA-Z0-9]', '', query).lower()
#         mycursor.execute("SELECT * FROM Users WHERE lower(screen_name)=%s", (query,))
#         user = mycursor.fetchone()

#         if user:
#             results = tweets_collection.find({"user.id_str": str(user[0])}).limit(10)
#             tweets = list(results)
#             return render_template('search_results.html', tweets=tweets)
#         else:
#             return "User not found."

#     elif search_type == 'hashtag':
#         query = re.sub(r'[^a-zA-Z0-9]', '', query)
#         results = tweets_collection.find({"entities.hashtags.text": {"$regex": f"(?i)^{query}"}}).limit(10)
#         tweets = list(results)
#         return render_template('search_results.html', tweets=tweets)

#     else:
#         return "Invalid search type."

# if __name__ == '__main__':
#     app.run(debug=True)
