from db import db

class EnrollmentModel(db.Model):
    __tablename__ = "enrollments"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    student = db.relationship('StudentModel', back_populates='enrollments')
    course = db.relationship('CourseModel', back_populates='enrollments')
