import uuid
from flask import Blueprint, json, request, jsonify
from chatScripts.parseComplaint import processComplaint
from model import db, User, Entry
from werkzeug.utils import secure_filename
import os
import textract
from updateDatabase.updateDb import updateDB

text_bp = Blueprint('text_bp', __name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'complaintUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@text_bp.route('/textQuery', methods=['POST', 'OPTIONS'])
def handle_prompt():
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
    

    if 'complaintFile' not in request.files:
        return jsonify({"error": "No file part"}), 400

    # data = request.json 
    # prompt = data.get('prompt')
    # clerk_id = data.get('clerkId')

    file_type = 'TEXT'


    file = request.files['complaintFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file to the temporary folder
        file.save(file_path)


        # Extract text from the file
        text = textract.process(file_path).decode('utf-8')

        print('THIS IS THE TEXT: \n\n***', text)

        # Clean up the temporary file
        os.remove(file_path)

        # Extract clerkId from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid or missing Authorization header"}), 401

        clerk_id = auth_header.split(' ')[1]

        if not text:
            return jsonify({"error": "No text extracted from file"}), 400

        # Fetch the user from the database
        user = User.query.filter_by(clerkId=clerk_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Process the complaint using AI
        result = processComplaint(text)

        # Update the database with the result
        return updateDB(file_type, text, user, result)

