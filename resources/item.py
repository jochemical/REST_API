
# Imports
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
# from db import stores
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

# A blueprint is used to seperate the API in segments
blp = Blueprint("Items", __name__, description="Operations on items") # first arg is name, second arg import name, description 


# MethodView enables to use the same endpoint for different method views (get, post, delete, etc.)
# Routes for specific items (using item_id)
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    
    # Get item
    @jwt_required()
    @blp.response(200, ItemSchema) # status code 200, Second argument is the ouput of the dataAPI
    def get(self, item_id):
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found.")

        # Get item from database
        # Query is build in SQLAlchemy to call an item based on the primary key
        item = ItemModel.query.get_or_404(item_id)
        return item

    # Delete item
    @jwt_required()
    def delete(self, item_id):

        # Get information stored within the jwt
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)

        
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

        # raise NotImplementedError("Deleting an item is not implemented.")
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted."}
        # except KeyError:
        #     print("ERROR: The item you want to delete is not found.")
        #     abort(404, message="Item not found.")
    
    # Update item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema) # Keep this order!
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        # raise NotImplementedError("Updating an item is not implemented.")

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item

        # Note that the argument of the decorator item_data needs to be in front of the route-argument item_id

        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     print("ERROR: price or name is missing in the item data.")
        #     abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")
        
        # try:
        #     item = items[item_id]
        #     item |= item_data
        #     # |= is an update operator, replaces the original dictionary!
        #     return item
        # except KeyError:
        #     print("ERROR: Item to update not found.")
        #     abort(404, message="Item not found.")

# Routes for non-specific items
@blp.route("/item")
class ItemList(MethodView):

    # Endpoint to get all items
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all() # many=True enables to accept a list
    #   return items.values()
    
    # Endpoint to create new item
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema) # Here we decorate the function with a schema for datavalidation
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        # item_data is a JSOn validated by schemas
        
        # To get the posted JSON file, we use request from Python
        # item_data = request.get_json()
        

        # # Check if data exists
        # if (
        #     "price" not in item_data 
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     print("Error: Missing keyword in posted item.")
        #     abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload.")

        # Check if item already exists
        # for item in items.values():
        #     if (
        #         item_data["name"] == item["name"]
        #         and item_data["store_id"] == item["store_id"]
        #     ):
        #         print("Error: Item already exists.")
        #         abort(400, message=f"Item already exists.")

        # # Check if store is in database
        # if item_data["store_id"] not in stores:
        #     # Return a 404 error with message (build in function of flask_smorest to add documentation)
        #     abort(404, message="Store not found.")    

        # # Create item_id
        # item_id = uuid.uuid4().hex

        # # Add item to new dict
        # item = {**item_data, "id": item_id}

        # # Add new item to our items dict
        # items[item_id] = item


        item = ItemModel(**item_data)
        # ** will change a dict to keyword-arguments

        try:
            # Insert in database, id created
            db.session.add(item) # First add, then commit
            db.session.commit() # After commit, it will be actually added to the database
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        # Return added item and 201 status code
        return item 




