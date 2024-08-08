# This Pythonfile is for data-validation
# Here we define how data should behave

# Imports
import re
from marshmallow import Schema, fields


# Here we define how datafields will behave as input and/or output
class PlainItemSchema(Schema):

    # Dump_only means we only use this field to retrieve data, not to accept
    id = fields.Str(dump_only=True)

    # Required means this field must be non-empty
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    # store_id = fields.Str(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

# Plain Tag
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True) # Dump_only means we only use this field to retrieve data, not to accept
    name = fields.Str()


# Data requirements for updating an item
class ItemUpdateSchema(Schema):
    
    # The user might send us these two fields, but maybe none
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

# When creating a store
class PlainStoreSchema(Schema):

    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    # Only when we get data from the client
    store_id = fields.Int(required=True, load_only=True)

    # For returning data to the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    # with PlainStoreSchema() we also add store fields of PlainStoreSchema

    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True )

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

# Tag Schema
class TagSchema(PlainTagSchema):
    # Only when we get data from the client
    store_id = fields.Int(load_only=True)

    # For returning data to the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    # with PlainStoreSchema() we also add store fields of PlainStoreSchema

    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True ) # Very important!
    
