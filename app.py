# ------------------ Small REST-API for stores and items ------------------------- #


# --------------------------- Imports ----------------------- #

# import uuid
import os # To get environment variables, for example to get the database URI
import secrets
import models 
# To get easy acces to our models. __init__.py in models is called automatically during import.
# This import has to be done before creating the Flask app with app=Flask(__name__)

from dotenv import load_dotenv

from flask import Flask, jsonify #, request
from flask_smorest import Api, abort
from db import db # To import our (SQLAlchemy-database)
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_migrate import Migrate
# from db import items, stores

# Import blueprints
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


# --------------------------- Create Flask App -------------------------- #

# Function to create Flask-app (build in the library) (the factory pattern)
# - It is better to use a function for testing e.a.
# - One optional argument to pass in an url for the database
def create_app(db_url=None):
    
    # Create app
    app = Flask(__name__)

    # Configurations for API
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configure for Database
    # - In general we use a connection string to connect the client to the database
    # - Possible databases are for example SQLite (easy and fast) and PostGreSQL
    # - If no database is given, we use a sqlite database with the name data.db
    # - With os.getenv() we search for an environment variable, if it does not excist the second argument is used.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This is not really important
    
    # Connect the Flask app to SQLAlchemy !
    db.init_app(app) 

    migrate = Migrate(app, db)

    # Create API
    api = Api(app)

    # app.config["JWT_SECRET_KEY"] = secrets.SystemRandom().getrandbits(128)
    # app.config["JWT_SECRET_KEY"] = ""
    # Keys has to be stored within environment variables

    # Added by myself
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    jwt = JWTManager(app)

    # Check if token is in blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # If toke is in blocklist the following error is send
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "The toke has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # Specific decorator for Fresh tokens
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401
        )

    # To add extra information for each acces token
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message": "Signature verificatoin failed.", "error": "invalid_token"}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {
                    "description": "Request does not contain an access token.", 
                    "error": "authorization_required"
                }
            ),
            401,
        )

    # Before Flask gets the first request, the SQL-tables has to be created.
    # @app.before_first_request
    # def create_tables():
    #     db.create_all

    # Not necesary if we use Flask-migrate
    # with app.app_context():
    #     db.create_all()
    
    # Register Blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)


    # Return the app
    return app







# # ------------------------------- Endpoints / Routes --------------------------------- #


# # ------------ Routes for Stores ------------- #

# # Endpoint to get data about all stores (called by request http://.../store ) #
# @app.get("/store") # this is equal to @app.route("/store", methods=["GET"])
# def get_stores():
#     # We send the browser the store-data as a dict
#     return {"stores": list( stores.values() ) }

#     # Note we create a list
#     # Note that 'stores' is recognised as global variable


# # Endpoint to get information about a SPECIFIC store #
# @app.get("/store/<string:store_id>") # @app.route("/store/<string:store_id>", methods=["GET"])
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         # Return error message and status code if store is not found
#         abort(404, message="Store not found.")


# # Endpoint to create a new store #
# @app.post("/store") # is equal to @app.route("/store", methods=["POST"]) 
# def create_store():
#     # To get the posted JSON file, we use request from Python
#     store_data = request.get_json()
#     # store_data will be a dictionary (from a JSON) which includes all stores
#     # (JSON files are strings, not dictionaries)

#     # Data validation
#     if "name" not in store_data:
#         # There must be a name inside the posted JSON
#         print("Error: The store has no name.")
#         abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
#     for store in stores.values():
#         # The name of the new store must be unique
#         if store_data["name"] == store["name"]:
#             print("Error: Store already exists.")
#             abort(400, message=f"Store already exists.")

#     # Create random id number 
#     store_id = uuid.uuid4().hex

#     # Use this data to create the new store
#     store = {**store_data, "id": store_id}

#     # Add the new_store to our store database / JSON for stores
#     stores[store_id] = store # Add new element to dictionary

#     # Return the added store and the 201 status code meaning: data accepted
#     return store, 201


# # Endpoint for deleting stores 
# @app.delete("/store/<string:item_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         print("ERROR: The store you want to delete is not found.")
#         abort(404, message="Store not found.")



# # ------------ Routes for Items ------------- #

# # Endpoint to create new items in excisting store #
# # <string:name> dynamic URL-segment (alternative is a query-string parameter)
# # name is the variable where the dynamic URL-segment is stored in
# @app.post("/item") # @app.route("/item", methods=["POST"])
# def create_item():
#     # To get the posted JSON file, we use request from Python
#     item_data = request.get_json()

#     # ------- Data-validation -------- #
#     # Check if data exists
#     if (
#         "price" not in item_data 
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         print("Error: Missing keyword in posted item.")
#         abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload.")

#     # Check if item already exists
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             print("Error: Item already exists.")
#             abort(400, message=f"Item already exists.")

#     # Check if store is in database
#     if item_data["store_id"] not in stores:
#         # Return a 404 error with message (build in function of flask_smorest to add documentation)
#         abort(404, message="Store not found.")    
#     # --------------- end datavalidation ---------- #

#     # Create item_id
#     item_id = uuid.uuid4().hex

#     # Add item to new dict
#     item = {**item_data, "id": item_id}

#     # Add new item to our items dict
#     items[item_id] = item

#     # Return added item and 201 status code
#     return item, 201


# # Endpoint for deleting items 
# # app.route("/item/<string:item_id>", methods=["DELETE"])
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted."}
#     except KeyError:
#         print("ERROR: The item you want to delete is not found.")
#         abort(404, message="Item not found.")


# # Endpoint to get all items
# @app.get("/item") #@app.route("/item", methods=["GET"])
# def get_all_items():
#     return {"items": list( items.values() ) }


# # Endpoint to get information about a specific item #
# @app.get("/item/<string:item_id>") # @app.route("/item/<string:item_id>", methods=["GET"])
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Item not found.")


# # Update item
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         print("ERROR: price or name is missing in the item data.")
#         abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")
    
#     try:
#         item = items[item_id]
#         item |= item_data
#         # |= is an update operator, replaces the original dictionary!
#         return item
#     except KeyError:
#         print("ERROR: Item to update not found.")
#         abort(404, message="Item not found.")
