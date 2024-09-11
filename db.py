
# Imports

# flask_sqlalchemy is an Flask-extension for better use of SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy object
# - Later on we link this object to our Flask-app
db = SQLAlchemy()


# # Pythonfile for databases

# items = {}
# stores= {}


# # Stores in a Jason-file (JSON, often used for REST-API's) (a dict for each store)
# # A JSON file is a list or dict/object turned into a string (True -> true, whitespaces removed)
# # stores = [
# #     {
# #         "name": "My Store",
# #         # A list for all items, a dict for each individual item
# #         "items": [
# #             {
# #                 "name": "Chair",
# #                 "price": 15.99
# #             }
# #         ]
# #     }
# # ]