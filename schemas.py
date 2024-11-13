# src/schema.py
from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    
    
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))
    
class StoreUpdateSchema(Schema):
    name = fields.Str()
    
    
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))
    
class TagAndItemSchema(Schema):
    message=fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
#--------------------------------------------------
class PlainStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)
    email = fields.Email(required=True)
    mobileNumber = fields.Str(
        required=True,
    )
    DOB = fields.Date(required=True, format="%m/%d/%Y")

class PlainCoursesSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    

class EnrollmentSchema(Schema):
    course_id = fields.Int(required=True, description="ID of the course to enroll in")



import base64

class FileSchema(Schema):
    id = fields.Int()
    filename = fields.Str()

    # Optionally, base64 encode pdf_file for small files (not recommended for large files)
    pdf_file = fields.Method("get_pdf_base64")

    def get_pdf_base64(self, obj):
        # This assumes obj is a FileModel instance
        return base64.b64encode(obj.pdf_file).decode('utf-8') if obj.pdf_file else None
