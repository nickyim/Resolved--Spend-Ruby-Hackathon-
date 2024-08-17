import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
from chatScripts.parseComplaint import processComplaint
from enum import Enum


app = Flask(__name__)
CORS(app)

load_dotenv()

# Corrected configuration key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)

class FileType(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    AUDIO = 'AUDIO'
    JSON = 'JSON'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clerkId = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entryId = db.Column(db.String, unique=True, nullable=False)
    isComplaint = db.Column(db.Boolean, nullable=False)
    product = db.Column(db.String)
    subProduct = db.Column(db.String)
    issue = db.Column(db.String)
    subIssue = db.Column(db.String)
    entryText = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String)
    dateSentToCompany = db.Column(db.DateTime)
    dateReceived = db.Column(db.DateTime)
    company = db.Column(db.String)
    companyResponse = db.Column(db.String)
    companyPublicResponse = db.Column(db.String)
    consumerDisputed = db.Column(db.String)
    consumerConsentProvided = db.Column(db.String)
    state = db.Column(db.String)
    zipCode = db.Column(db.String)
    submittedVia = db.Column(db.String)
    tags = db.Column(db.String)
    timely = db.Column(db.Boolean)
    productCategory = db.Column(db.String)
    subProductCategory = db.Column(db.String)
    vectorId = db.Column(db.String)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    files = db.relationship('File', backref='entry', lazy=True)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(FileType), nullable=False)
    entryId = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    clerk_id = data.get('clerkId')
    email = data.get('email')

    if not clerk_id or not email:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(clerkId=clerk_id).first():
        return jsonify({"error": "User already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

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
    }), 200

@app.route('/test', methods=['POST'])
def test_post():
    data = request.json
    response = {
        'message': 'Data received!',
        'data': data
    }
    return jsonify(response), 200

@app.route('/api/prompt', methods=['POST', 'OPTIONS'])
def handle_prompt():
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
    
    data = request.json 
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # TODO: add logic to process prompt, save it to db 

    result = processComplaint(prompt)

    print(f"Received prompt: {result}")

    return jsonify({"message": "Prompt received successfully", "prompt": result}), 200


if __name__ == '__main__':
    app.run(debug=True) # remove debug=True for production