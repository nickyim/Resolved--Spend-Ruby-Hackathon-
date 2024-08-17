
import os
from flask import Blueprint, json, request, jsonify
from chatScripts.processAudio import processAudio
from werkzeug.utils import secure_filename

audio_bp = Blueprint('audio_bp', __name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'complaintUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@audio_bp.route('/audioQuery', methods=['POST'])
def upload_audio():
    if 'audioFile' not in request.files:
        return jsonify({"error": "No audio file part"}), 400

    file = request.files['audioFile']

    print(f"\n\nReceived audio file: {file.filename} \n\n ********")

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Extract the file extension
        file_extension = os.path.splitext(file.filename)[1]
        # Force the filename to be userComplaint with the original extension
        filename = secure_filename(f"userComplaint{file_extension}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file to the temporary folder
        file.save(file_path)

        try:
            # Pass the file path to the processAudio function
            result = processAudio(file_path)

            print(f"Received Audio result: {result}")

            return jsonify({"message": "Audio file processed successfully", "result": result}), 200
        finally:
            # Delete the file after processing
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
