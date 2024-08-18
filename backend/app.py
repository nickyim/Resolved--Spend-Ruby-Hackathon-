import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from model import db, User, Entry
from routes.user_routes import user_bp
from routes.text_routes import text_bp
from routes.audio_routes import audio_bp
from routes.video_routes import video_bp
from routes.dashboard_routes import dashboard_bp
from routes.elastic_routes import elastic_bp
from routes.image_routes import image_bp

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
gcs_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
gcs_bucket = os.getenv('CLOUD_STORAGE_BUCKET')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Log the environment variables (for debugging purposes)
logging.info(f"Google Application Credentials: {gcs_credentials}")
logging.info(f"Google Cloud Storage Bucket: {gcs_bucket}")


app = Flask(__name__)
CORS(app)

# Corrected configuration key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # Properly initialize the SQLAlchemy instance with the Flask app
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(text_bp, url_prefix='/api')
app.register_blueprint(audio_bp, url_prefix='/api')
app.register_blueprint(video_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')
app.register_blueprint(elastic_bp, url_prefix='/api')
app.register_blueprint(image_bp, url_prefix='/api')


@app.route('/test', methods=['POST'])
def test_post():
    data = request.json
    response = {
        'message': 'Data received!',
        'data': data
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True) # remove debug=True for production