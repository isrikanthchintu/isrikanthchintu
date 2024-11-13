from db import db
from sqlalchemy import Column, Integer, LargeBinary

class FileModel(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    pdf_file = db.Column(db.LargeBinary, nullable=False)
