import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)