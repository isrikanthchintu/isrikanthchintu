# resources/item.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
            
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            abort(404, message="Item not found.")

        item.name = item_data.get("name", item.name)
        item.price = item_data.get("price", item.price)
        item.store_id = item_data.get("store_id", item.store_id)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while updating the item: {str(e)}")

        return item

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="An item with this name already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while inserting the item: {str(e)}")
        return item
