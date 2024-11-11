from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.course import CourseModel
from schemas import PlainCoursesSchema

blp = Blueprint("Courses", 'courses', description= "Operations on Courses")

@blp.route("/course")
class CourseList(MethodView):
    @blp.response(200, PlainCoursesSchema(many=True))
    def get(self):
        return CourseModel.query.all()
    
    @blp.arguments(PlainCoursesSchema)
    @blp.response(201, PlainCoursesSchema)
    def post(self, course_data):
        course = CourseModel(**course_data)
        try:
            db.session.add(course)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A course with this Identifier already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the course.")
            
            
@blp.route("/course/<int:course_id>")
class CourseDetail(MethodView):
    @blp.response(200, PlainCoursesSchema)
    def get(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        return course
    
    def delete(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted"}
    
    
    @blp.arguments(PlainCoursesSchema)
    @blp.response(200, PlainCoursesSchema)
    def put(self,course_data, course_id):
        course = CourseModel.query.get_or_404(course_id)
        course.name = course_data.get("name", course.name)
        course.description = course_data.get("description", course.description)
        
        db.session.commit()
        return course
    