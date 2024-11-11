from db import db
from sqlalchemy.orm import relationship

class CourseModel(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    
    # Many-to-Many relationship with Students
    students = relationship('StudentModel', secondary='enrollments', back_populates='courses')
    
    # One-to-Many relationship with enrollments
    enrollments = relationship('EnrollmentModel', back_populates='course')
