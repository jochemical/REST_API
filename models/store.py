# Imports
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(80), unique=True, nullable=False)

    # To poppulate the items variable, SQLAlchemy uses the id variable of the store
    # which is defined above.
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic") #, cascade="all, delete")
    # lazy=dynamic makes sure items is only poppulates when we ask for it
    # cascade="all, delete" makes sure that if we delete a store, the items inside it will also be deleted.

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    # back_populates="store" --> store has to match with the relationship in TagModel !
    # lazy="dynamic" makes sure your code runs faster, otherwise the database will be fetched when a new classobject is created
    
    