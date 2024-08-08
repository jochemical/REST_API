# Import the database db (a SQLAlchemy object, or instance)
from db import db
# we can use this db-object to define which tables we want to use and
# to define the columns within these tables.

# If we create a class which maps to a table with columns, 
# each row will become an python-object.
# A mapping between a table-ROW and a Pythonclass/Pythonobject
# An object from this class is a ROW within the table db.Model
class ItemModel(db.Model):
    # Create a table called 'items' for each object of this class
    __tablename__ = "items"

    # Define columns in this table
    id = db.Column(db.Integer, primary_key=True)
    # db.Integer is auto-incrementing, so each new object will get the next unused number
    
    name = db.Column(db.String(80), unique=False, nullable=False)
    # db.String(80) means a string with max 80 characters, nullabe means that a name is mandatory
    description = db.Column(db.String)

    price = db.Column( db.Float(precision=2), unique=False, nullable=False )
    
    store_id = db.Column( db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False )
    # With foreignKey you tell python that this key refers/maps/relates to a COLUMN(!) in another table
    # stores.id means the id-column of the stores-table
    # store_id has to match one of the id-number of the stores (one-to-many)
    # Therefore we use db.ForeignKey, which also makes sure that 
    # an item cannot be create if there is not a corresponding id in stores.id to link to.
    # This last note is not the case if we use SQLite
    
    # Now we want to grab a store(model)-classobject which has the store-id we are looking for
    # So we are actually  grabbing the ROW which has this store-id within the store-table
    store = db.relationship("StoreModel", back_populates="items")
    # So we add a variabel (called store) to each itemclass-object which remembers the storeclass-object where the item is linked to.
    # Somehow SQLAlchemy knows we are aiming for the store_id selected above, because
    # stores.id uses StoreModel
    # back_populates="items" is needed to fill/poppulate the items variable of the store-object, so when we create a new item...
    # the storeclassobject 'gets' the itemclassobject as well, so immediatly we also add something to the related storeclassobject
    # This is logical, because when an new item is created, we have to 'put' the item also in the storeclassobject (within the store-stable in the column for items )

    # Related tags to this item (many-to-many relationship)
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
