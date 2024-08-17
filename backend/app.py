import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()

# Corrected configuration key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)

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
    
    #TODO: add logic to process prompt, save it to db 
    print(f"Received prompt: {prompt}")

    return jsonify({"message": "Prompt received successfully", "prompt": prompt}), 200


if __name__ == '__main__':
    app.run(debug=True) # remove debug=True for production