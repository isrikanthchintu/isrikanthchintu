# src/create_db.py
from app import create_app
from db import db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database and tables created successfully.")