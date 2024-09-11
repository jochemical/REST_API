# Imports
# from sqlite3 import IntegrityError
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db

from models import StoreModel


from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import StoreSchema

# A blueprint is used to seperate the API in segments
blp = Blueprint("stores", __name__, description="Operations on stores") # first arg is name, second arg import name, description 


# MethodView enables to use the same endpoint for different method views (get, post, delete, etc.)
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    
    # Get store
    @blp.response(200, StoreSchema)    
    def get(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            return store
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     # Return error message and status code if store is not found
        #     abort(404, message="Store not found.")
    
    # Delete store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted"}
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message="Integrity error occurred: (store contains items!) " + str(e))
        # raise NotImplementedError("Deleting a store is not implemented.")

        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     print("ERROR: The store you want to delete is not found.")
        #     abort(404, message="Store not found.")


# A different endpoint for all the stores
@blp.route("/store")
class StoreList(MethodView):

    # Get all stores
    @blp.response(201, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        # return stores.values()

    # Create new store
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # To get the posted JSON file, we use request from Python
        # store_data = request.get_json()
        # store_data will be a dictionary (from a JSON) which includes all stores
        # (JSON files are strings, not dictionaries)

        # # Data validation
        # if "name" not in store_data:
        #     # There must be a name inside the posted JSON
        #     print("Error: The store has no name.")
        #     abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        # for store in stores.values():
        #     # The name of the new store must be unique
        #     if store_data["name"] == store["name"]:
        #         print("Error: Store already exists.")
        #         abort(400, message=f"Store already exists.")

        # # Create random id number 
        # store_id = uuid.uuid4().hex

        # # Use this data to create the new store
        # store = {**store_data, "id": store_id}

        # # Add the new_store to our store database / JSON for stores
        # stores[store_id] = store # Add new element to dictionary

        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")


        # Return the added store and the 201 status code meaning: data accepted
        return store #, 201