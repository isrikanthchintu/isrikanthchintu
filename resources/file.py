import os
import uuid
import logging
from datetime import datetime
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError

from models import FileModel
from schemas import FileSchema
from db import db

import csv
import io
from flask import Response

blp = Blueprint("files", "Files", description="Operations on files")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

file_schema = FileSchema()
files_schema = FileSchema(many=True)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @blp.route('/upload')
# class FileUploadResource(MethodView):
#     @blp.response(201, FileSchema)
#     def post(self):
#         # Check for file in request
#         if 'file' not in request.files:
#             logger.error("No file part in the request.")
#             abort(400, message="No file part in the request.")

#         file = request.files['file']
        
#         # Check if no file is selected
#         if file.filename == '':
#             logger.error("No file selected for uploading.")
#             abort(400, message="No file selected.")

#         # Validate file extension (only PDF allowed)
#         if file and file.filename.endswith('.pdf'):
#             filename = f"{uuid.uuid4().hex}.pdf"  # Generate unique filename
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
            
#             try:
#                 # Save the file
#                 file.save(filepath)
                
#                 # Create a new file record in the database (without the upload_timestamp)
#                 new_file = FileModel(filename=filename)  # Removed upload_timestamp
#                 db.session.add(new_file)
#                 db.session.commit()
#                 logger.info(f"File {filename} uploaded successfully.")
                
#                 # Return the serialized file data as a response
#                 return file_schema.dump(new_file), 201
#             except SQLAlchemyError as e:
#                 db.session.rollback()
#                 logger.error(f"Database error: {str(e)}")
#                 abort(500, message="An error occurred while saving the file.")
#         else:
#             logger.warning("Invalid file format.")
#             abort(400, message="Only PDF files are allowed.")


# @blp.route('/upload')
# class FileUploadResource(MethodView):
#     @blp.response(201, FileSchema)
#     def post(self):
#         # Check for file in the request
#         if 'file' not in request.files:
#             logger.error("No file part in the request.")
#             abort(400, message="No file part in the request.")

#         file = request.files['file']

#         # Check if no file is selected
#         if not file.filename:
#             logger.error("No file selected for uploading.")
#             abort(400, message="No file selected.")

#         # Validate file extension (only PDF allowed)
#         if file and file.filename.lower().endswith('.pdf'):
#             filename = f"{uuid.uuid4().hex}.pdf"  # Generate unique filename
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
            
#             try:
#                 # Save the file to the designated upload folder
#                 file.save(filepath)
                
#                 # Create a new file record in the database without upload_timestamp
#                 new_file = FileModel(filename=filename)  # No upload_timestamp field in this example
#                 db.session.add(new_file)
#                 db.session.commit()
#                 logger.info(f"File {filename} uploaded and saved successfully.")

#                 # Sample patient data for the response
#                 patient_data = [
#                     {
#                         "dob": "2013-10-17",
#                         "first_name": "Jonny",
#                         "hospital": "St Andrews Hospital",
#                         "last_name": "Jenny",
#                         "procedure_date": "2024-11-09T10:00:00",
#                         "procedure_name": "Left Cataract",
#                         "prostheses": "Lens TorbiMP",
#                         "provider": "Tim Gray"
#                     },
#                     {
#                         "dob": "2013-10-17",
#                         "first_name": "Jonny",
#                         "hospital": "St Andrews Hospital",
#                         "last_name": "Jenny",
#                         "procedure_date": "2024-11-09T10:00:00",
#                         "procedure_name": "Left Cataract",
#                         "prostheses": "Lens TorbiMP",
#                         "provider": "Tim Gray"
#                     }
#                 ]

#                 # Serialize the file data
#                 response_data = FileSchema().dump(new_file)
                
#                 # Remove upload_timestamp if it exists
#                 response_data.pop('upload_timestamp', None)

#                 # Add patient data to the response
#                 response_data['patient_data'] = patient_data
                
#                 return jsonify(response_data), 201
            
#             except SQLAlchemyError as e:
#                 db.session.rollback()
#                 logger.error(f"Database error while saving file: {str(e)}")
#                 abort(500, message="An error occurred while saving the file.")
#         else:
#             logger.warning("Invalid file format. Only PDF files are allowed.")
#             abort(400, message="Only PDF files are allowed.")




@blp.route('/upload')
class FileUploadResource(MethodView):
    @blp.response(201, FileSchema)
    def post(self):
        if 'file' not in request.files:
            logger.error("No file part in the request.")
            abort(400, message="No file part in the request.")
        
        file = request.files['file']
        
        if not file.filename:
            logger.error("No file selected for uploading.")
            abort(400, message="No file selected.")
        
        # Check file type and size
        if file.content_type != 'application/pdf':
            logger.warning("Invalid file format. Only PDF files are allowed.")
            abort(400, message="Only PDF files are allowed.")
        
        MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB
        if len(file.read()) > MAX_FILE_SIZE:
            logger.warning("File size is too large.")
            abort(400, message="File size exceeds the 16MB limit.")
        
        filename = f"{uuid.uuid4().hex}.pdf"
        
        try:
            file.seek(0)  # Rewind the file after reading its size
            pdf_data = file.read()
            
            new_file = FileModel(filename=filename, pdf_file=pdf_data)
            db.session.add(new_file)
            db.session.commit()
            logger.info(f"File {filename} uploaded and saved successfully.")
            
            # Sample patient data
            patient_data = [
                {
                    "dob": "2013-10-17",
                    "first_name": "Jonny",
                    "hospital": "St Andrews Hospital",
                    "last_name": "Jenny",
                    "procedure_date": "2024-11-09T10:00:00",
                    "procedure_name": "Left Cataract",
                    "prostheses": "Lens TorbiMP",
                    "provider": "Tim Gray"
                },{
                    "dob": "2013-10-17",
                    "first_name": "Jonny",
                    "hospital": "St Andrews Hospital",
                    "last_name": "Jenny",
                    "procedure_date": "2024-11-09T10:00:00",
                    "procedure_name": "Left Cataract",
                    "prostheses": "Lens TorbiMP",
                    "provider": "Tim Gray"
                },{
                    "dob": "2013-10-17",
                    "first_name": "Jonny",
                    "hospital": "St Andrews Hospital",
                    "last_name": "Jenny",
                    "procedure_date": "2024-11-09T10:00:00",
                    "procedure_name": "Left Cataract",
                    "prostheses": "Lens TorbiMP",
                    "provider": "Tim Gray"
                },{
                    "dob": "2013-10-17",
                    "first_name": "Jonny",
                    "hospital": "St Andrews Hospital",
                    "last_name": "Jenny",
                    "procedure_date": "2024-11-09T10:00:00",
                    "procedure_name": "Left Cataract",
                    "prostheses": "Lens TorbiMP",
                    "provider": "Tim Gray"
                },{
                    "dob": "2013-10-17",
                    "first_name": "Jonny",
                    "hospital": "St Andrews Hospital",
                    "last_name": "Jenny",
                    "procedure_date": "2024-11-09T10:00:00",
                    "procedure_name": "Left Cataract",
                    "prostheses": "Lens TorbiMP",
                    "provider": "Tim Gray"
                },{
                    "dob": "2013-10-17",
                    "first_name": "Jonny",
                    "hospital": "St Andrews Hospital",
                    "last_name": "Jenny",
                    "procedure_date": "2024-11-09T10:00:00",
                    "procedure_name": "Left Cataract",
                    "prostheses": "Lens TorbiMP",
                    "provider": "Tim Gray"
                }
            ]
            
            response_data = FileSchema().dump(new_file)
            response_data.pop('upload_timestamp', None)
            response_data['patient_data'] = patient_data
            
            return jsonify(response_data), 201
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while saving file: {str(e)}")
            abort(500, message="An error occurred while saving the file.")




@blp.route('/files/<int:file_id>')
class FileDownloadResource(MethodView):
    def get(self, file_id):
        # Query the file from the database
        file = FileModel.query.get(file_id)
        
        if not file:
            abort(404, message="File not found.")
        
        # Send the file as a response
        return jsonify({
            'filename': file.filename,
            'pdf_file': file.pdf_file.decode('latin1')  
        }), 200



@blp.route('/files')
class FileListResource(MethodView):
    @blp.response(200, FileSchema(many=True))
    def get(self):
        try:
            # Retrieve all file records from the database
            files = FileModel.query.all()  # Retrieve all files, or apply a filter as needed
            logger.info(f"Retrieved {len(files)} files.")
            return files_schema.dump(files), 200
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving files: {str(e)}")
            abort(500, message="Error retrieving files.")


@blp.route('/files/csv')
class FileListCSVResource(MethodView):
    def get(self):
        try:
            # Retrieve all file records from the database
            files = FileModel.query.all()  # Retrieve all files, or apply a filter as needed
            logger.info(f"Retrieved {len(files)} files.")

            # Prepare the CSV file content
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["id", "filename"])  # Exclude upload_timestamp here
            writer.writeheader()  # Write header row

            # Write data rows to the CSV
            for file in files:
                file_data = {
                    "id": file.id,
                    "filename": file.filename,
                }
                writer.writerow(file_data)

            # Get CSV data from the StringIO object
            csv_data = output.getvalue()
            output.close()

            # Return CSV data as a downloadable file
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={"Content-Disposition": "attachment;filename=files_data.csv"}
            )
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving files for CSV export: {str(e)}")
            abort(500, message="Error retrieving files for CSV export.")