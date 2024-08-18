
import os
from flask import Blueprint, json, request, jsonify
from chatScripts.processAudio import processAudio
from chatScripts.googleAudioProcess import transcribe_audio
from werkzeug.utils import secure_filename
from google.cloud import storage
from google.cloud import speech


audio_bp = Blueprint('audio_bp', __name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'complaintUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@audio_bp.route('/assemblyaiAudioQuery', methods=['POST'])
def upload_audio():
    if 'complaintFile' not in request.files:
        return jsonify({"error": "No audio file part"}), 400

    file = request.files['complaintFile']

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
                

@audio_bp.route('/googleAudioQuery', methods=['GET', 'POST'])
def upload_audio2Google():
    # Get the audio file from the request.
    audio = request.files['complaintFile']
    audio_content = audio.read()

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

    print(f"\n\nReceived Google Audio result: {results}\n\n********")
    
    # Return the results as a JSON response.
    return jsonify({"message": "Audio file processed successfully", "result": results}), 200