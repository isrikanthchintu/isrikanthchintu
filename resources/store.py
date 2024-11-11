# resources/store.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema

# Define the blueprint for store-related operations
blp = Blueprint("Stores", "stores", description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """Retrieve a store by its ID."""
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        """Delete a store by its ID."""
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        """
        Update a store by its ID.
        Fields are updated only if provided in the request data.
        """
        store = StoreModel.query.get_or_404(store_id)

        # Update only fields that are present in the input data
        store.name = store_data.get("name", store.name)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while updating the store.")

        return store

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Retrieve a list of all stores."""
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        """Create a new store with the provided data."""
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with this identifier already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store.")
        return store
