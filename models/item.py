# models/item.py
from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationship with StoreModel
    store = db.relationship("StoreModel", back_populates="items")
    
    # Many-to-many relationship with TagModel through the items_tags table
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
