import uuid
from flask import Blueprint, json, request, jsonify
from google.cloud import vision
from accessDatabase.updateDb import updateDB
from model import db, User, Entry
from werkzeug.utils import secure_filename
from chatScripts.parseComplaint import processComplaint  # Import your OpenAI function
from routes.elastic_routes import sync_data
import os

# Initialize the Blueprint
image_bp = Blueprint('image_bp', __name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'imageUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'pdf', }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route('/imageQuery', methods=['POST', 'OPTIONS'])
def handle_image():
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
    
    if 'imageFile' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['imageFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file to the temporary folder
        file.save(file_path)

        # Initialize Google Cloud Vision client
        client = vision.ImageAnnotatorClient()

        # Load the image into memory
        with open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Perform text detection on the image
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if not texts:
            return jsonify({"error": "No text detected in the image"}), 400
        
        text = texts[0].description
        print('Extracted Text from Image: \n\n***', text)

        # Clean up the temporary file
        os.remove(file_path)

        # Extract clerkId from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid or missing Authorization header"}), 401

        clerk_id = auth_header.split(' ')[1]

        # Fetch the user from the database
        user = User.query.filter_by(clerkId=clerk_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Process the extracted text using AI
        result = processComplaint(text)

        # Update the database using the updateDB function
        response = updateDB('IMAGE', text, user, result)

        # Sync the data with Elasticsearch after the database is updated
        sync_data()
    
        return response
