import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from chatScripts.parseComplaint import processComplaint
from chatScripts.processAudio import processAudio
from model import db, User, Entry, File
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

load_dotenv()

# Corrected configuration key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # Properly initialize the SQLAlchemy instance with the Flask app
migrate = Migrate(app, db)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    clerk_id = data.get('clerkId')
    email = data.get('email')

    if not clerk_id or not email:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(clerkId=clerk_id).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"error": "Email already exists"}), 400
    
    # Create new user
    new_user = User(clerkId=clerk_id, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/user', methods=['GET'])
def get_user():
    clerk_id = request.args.get('clerkId')

    if not clerk_id:
        return jsonify({"error": "No clerkId provided"}), 400

    user = User.query.filter_by(clerkId=clerk_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "clerkId": user.clerkId,
        "email": user.email
    })

@app.route('/test', methods=['POST'])
def test_post():
    data = request.json
    response = {
        'message': 'Data received!',
        'data': data
    }
    return jsonify(response), 200

@app.route('/api/textQuery', methods=['POST', 'OPTIONS'])
def handle_prompt():
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
    
    data = request.json 
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # TODO: add logic to process prompt, save it to db 

    result = processComplaint(prompt)

    print(f"Received text result: {result}")

    return jsonify({"message": "Prompt received successfully", "prompt": result}), 200

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'complaintUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/audioQuery', methods=['POST'])
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
    

if __name__ == '__main__':
    app.run(debug=True) # remove debug=True for production