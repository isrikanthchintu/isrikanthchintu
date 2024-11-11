# models/student.py

from db import db
from sqlalchemy import Column, Integer, String, Date,Column,Table
from sqlalchemy.orm import relationship


# #Association table for many-to-many relationship
# enrollment_association = Table(  
#     'enrollments',
#     db.Model.metadata,
#     db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
#     db.Column('course_id', db.Integer, db.ForeignKey('courses.id'),primary_key=True)
# )

class StudentModel(db.Model):
    __tablename__ = "students"
    
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobileNumber = db.Column(db.String(15))
    DOB = db.Column(db.Date)
    
    # Many-to-Many relationship with courses
    courses = relationship('CourseModel', secondary='enrollments', back_populates="students")
    
    # One-to-Many relationship with enrollments
    enrollments = relationship('EnrollmentModel', back_populates='student')
