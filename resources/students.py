# resources/student.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import StudentModel
from schemas import PlainStudentSchema

blp = Blueprint("Students", "students", description="Operations on Students")

@blp.route("/student")
class StudentList(MethodView):
    @blp.response(200, PlainStudentSchema(many=True))
    def get(self):
        return StudentModel.query.all()
    
    @blp.arguments(PlainStudentSchema)
    @blp.response(201, PlainStudentSchema)
    def post(self, student_data):
        student = StudentModel(**student_data)
        try:
            db.session.add(student)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A student with this identifier already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the student.")

@blp.route("/student/<int:student_id>")
class StudentDetail(MethodView):  # Renamed class for clarity
    @blp.response(200, PlainStudentSchema)
    def get(self, student_id):
        student = StudentModel.query.get_or_404(student_id)
        return student
    
    def delete(self, student_id):
        student = StudentModel.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}

    @blp.arguments(PlainStudentSchema)  # This decorator automatically handles the request data
    @blp.response(200, PlainStudentSchema)
    def put(self, student_data, student_id):
        # Fetch the student or return 404 if not found
        student = StudentModel.query.get_or_404(student_id)

        # Update the student's fields
        student.fname = student_data.get("fname", student.fname)
        student.lname = student_data.get("lname", student.lname)
        student.email = student_data.get("email", student.email)
        student.mobileNumber = student_data.get("mobileNumber", student.mobileNumber)

        try:
            db.session.commit()
        except IntegrityError:
            abort(400, message="A student with this identifier already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the student.")

        return student
