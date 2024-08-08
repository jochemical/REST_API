
from db import db

# This model is for many-to-many relationship between tags and items
class ItemTags(db.Model):
    # Table name
    __tablename__ = "items_tags"

    # Column
    id = db.Column(db.Integer, primary_key=True)

    # Note here we use two foreign keys
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))