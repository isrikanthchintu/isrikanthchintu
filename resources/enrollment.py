import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import StudentModel, CourseModel, EnrollmentModel
from schemas import EnrollmentSchema

# Initialize Blueprint
blp = Blueprint("Enrollments", "enrollments", description="Student enrollment operations")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@blp.route("/student/<int:student_id>/enroll")
class EnrollStudent(MethodView):
    @blp.arguments(EnrollmentSchema)
    @blp.response(201, EnrollmentSchema)
    def post(self, enrollment_data, student_id):
        """
        Enroll a student in a course.
        The request body must contain the course_id, and the student is identified by student_id in the URL.
        """
        # logger.debug(f"Request to enroll student with ID {student_id} in course.")
        
        # Fetch student and course
        student = StudentModel.query.get_or_404(student_id)
        # logger.debug(f"Found student: {student}")
        
        course = CourseModel.query.get_or_404(enrollment_data["course_id"])
        # logger.debug(f"Found course: {course}")

        # Check if the student is already enrolled in the course
        existing_enrollment = EnrollmentModel.query.filter_by(student_id=student.id, course_id=course.id).first()
        if existing_enrollment:
            # logger.debug(f"Student {student_id} is already enrolled in course {course.id}.")
            abort(400, message="Student is already enrolled in this course.")

        # Create a new enrollment
        enrollment = EnrollmentModel(student_id=student.id, course_id=course.id)
        logger.debug(f"Creating enrollment: {enrollment}")

        try:
            # logger.debug(f"Enrollment to be added: {enrollment}")
            db.session.add(enrollment)
            db.session.commit()
            # logger.info(f"Student {student_id} successfully enrolled in course {course.id}.")
        except SQLAlchemyError as e:
            db.session.rollback()
            # logger.error(f"Error while enrolling student {student_id} in course {course.id}: {str(e)}")
            abort(500, message=f"An error occurred while enrolling the student: {str(e)}")

        return enrollment
    
    
@blp.route("/student/<int:student_id>/enroll")
class GetStudentEnrollments(MethodView):
    @blp.response(200, EnrollmentSchema(many=True))
    def get(self, student_id):
        """
        Retrieve the list of enrollments for a given student.
        """
        logger.debug(f"Request to get enrollments for student with ID {student_id}.")
        
        # Fetch student
        student = StudentModel.query.get_or_404(student_id)
        # logger.debug(f"Found student: {student}")
        
        # Fetch enrollments for the student
        enrollments = EnrollmentModel.query.filter_by(student_id=student.id).all()
        if not enrollments:
            logger.debug(f"No enrollments found for student {student_id}.")
        
        logger.debug(f"Enrollments found: {enrollments}")
        
        # Return the list of enrollments
        return enrollments

