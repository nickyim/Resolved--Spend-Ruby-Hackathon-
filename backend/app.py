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


# create a test route
@app.route('/test', methods=['GET'])
def test():
  return jsonify({'message': 'The server is running'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)