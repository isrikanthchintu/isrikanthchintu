from db import db

class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    # Relationship with StoreModel
    store = db.relationship('StoreModel', back_populates='tags')
    
    # Many-to-many relationship with ItemModel through the items_tags table
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
