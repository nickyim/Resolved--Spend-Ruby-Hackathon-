import os
from flask import Blueprint, request, jsonify
from chatScripts.processAudio import processAudio
from chatScripts.googleAudioProcess import transcribe_audio
from werkzeug.utils import secure_filename
from google.cloud import storage
from google.cloud import speech
from accessDatabase.updateDb import updateDB
from model import db, User
import json
from routes.elastic_routes import sync_data

audio_bp = Blueprint('audio_bp', __name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'complaintUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_type = 'AUDIO'

@audio_bp.route('/assemblyaiAudioQuery', methods=['POST'])
def upload_audio():
    try:
        if 'audioFile' not in request.files:
            return jsonify({"error": "No audio file part"}), 400

        file = request.files['audioFile']
        print(f"Received audio file: {file.filename}")

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Extract clerkId from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid or missing Authorization header"}), 401

        try:
            clerk_id = auth_header.split(' ')[1].encode('ascii').decode('ascii')
        except UnicodeEncodeError:
            return jsonify({"error": "Authorization header contains non-ASCII characters"}), 400

        # Fetch the user from the database
        user = User.query.filter_by(clerkId=clerk_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Extract the file extension
        file_extension = os.path.splitext(file.filename)[1]
        # Force the filename to be userComplaint with the original extension
        filename = secure_filename(f"userComplaint{file_extension}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Save the file to the temporary folder
        file.save(file_path)
        print(f"File saved to {file_path}")

        try:
            # Pass the file path to the processAudio function
            result = processAudio(file_path)
            result_data = json.loads(result)
            text = result_data.get('summary', '')

            print(f"Processed audio result: {result}")

            # Update database
            return updateDB(file_type, text, user, result)

        finally:
            # Delete the file after processing
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@audio_bp.route('/googleAudioQuery', methods=['POST'])
def upload_audio2Google():
    try:
        if 'audioFile' not in request.files:
            return jsonify({"error": "No audio file part"}), 400

        # Get the audio file from the request
        audio = request.files['audioFile']

        if audio.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Extract clerkId from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid or missing Authorization header"}), 401

        clerk_id = auth_header.split(' ')[1]

        # Fetch the user from the database
        user = User.query.filter_by(clerkId=clerk_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Read the audio content from the file
        audio_content = audio.read()
        print(f"Read audio content, size: {len(audio_content)} bytes")

        # Determine the encoding based on the file extension
        file_extension = os.path.splitext(audio.filename)[1].lower()
        if file_extension == '.mp3':
            encoding = speech.RecognitionConfig.AudioEncoding.MP3
        elif file_extension == '.wav':
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
        else:
            return jsonify({"error": "Unsupported audio format"}), 400

        # Retrieve a Speech API response for the audio content
        results = transcribe_audio(audio_content, encoding)
        print(f"Received Google Audio result: {results}")

        result_data = json.loads(results)
        text = result_data.get('summary', '')

        # Update database
        response = updateDB(file_type, text, user, results)
    
        # Sync the data with Elasticsearch after the database is updated
        sync_data()

        return response


    except Exception as e:
        print(f"Error processing Google audio: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500