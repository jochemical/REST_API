from db import db

# Model inherits from db.Model
class TagModel(db.Model):

    # Name of table
    __tablename__ = "tags"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False) 
    # nullable=False -> no value is not allowed
    
    # The ForeignKey defines  
    # store_id = db.Column(db.String(), db.ForeignKey("stores.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates='tags')
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")


