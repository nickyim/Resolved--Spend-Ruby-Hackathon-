import os
import uuid
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from google.cloud import storage, videointelligence_v1 as videointelligence
import logging
from accessDatabase.updateDb import updateDB
from model import db, User, Entry
from chatScripts.classifyProductandSummarize import classifyProductandSummarize
from routes.elastic_routes import sync_data

video_bp = Blueprint('video_bp', __name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'videoUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@video_bp.route('/videoQuery', methods=['POST'])
def upload_video():
    if 'videoFile' not in request.files:
        logging.error("No video file part in request")
        return jsonify({"error": "No video file part"}), 400

    file = request.files['videoFile']
    clerk_id = request.form.get('clerkId')  # Get the user identifier from the form

    if file.filename == '':
        logging.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if not clerk_id:
        return jsonify({"error": "No clerkId provided"}), 400

    # Fetch the user from the database
    user = User.query.filter_by(clerkId=clerk_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if file:
        logging.info(f"Received file: {file.filename}")

        file_extension = os.path.splitext(file.filename)[1]
        filename = secure_filename(f"userComplaint{file_extension}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        try:
            logging.info(f"File saved to {file_path}")

            # Upload the video to Google Cloud Storage
            gcs_uri = upload_to_gcs(file_path, filename)
            logging.info(f"Uploaded to GCS: {gcs_uri}")

            # Process the video using Google Cloud Video Intelligence
            annotations = analyze_video(gcs_uri)
            logging.info(f"Video analysis result: {annotations}")

            # Use AI to decide if it's a complaint, categorize, and summarize
            complaint_result = analyze_complaint(annotations)  # Integration with classifyProduct happens here

            # Parse the result from the OpenAI API if it's returned as a string
            if isinstance(complaint_result, str):
                complaint_result = json.loads(complaint_result)

            # Use the updateDB function to store the entry in the database
            response = updateDB('VIDEO', complaint_result.get('summary', ''), user, json.dumps(complaint_result))

            # Sync the data with Elasticsearch after the database is updated
            sync_data()

            return response

        except Exception as e:
            logging.error(f"Error during video processing: {e}")
            return jsonify({"error": "Video processing failed"}), 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Deleted file: {file_path}")

def upload_to_gcs(file_path, filename):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket_name = os.environ.get('CLOUD_STORAGE_BUCKET')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(file_path)
    return f"gs://{bucket_name}/{filename}"

def analyze_video(gcs_uri):
    """Uses Google Cloud Video Intelligence to analyze a video."""
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [
        videointelligence.Feature.LABEL_DETECTION,
        videointelligence.Feature.SPEECH_TRANSCRIPTION
    ]

    try:
        logging.info(f"Starting video analysis for: {gcs_uri}")
        operation = client.annotate_video(
            request={
                "features": features,
                "input_uri": gcs_uri,
                "video_context": {
                    "speech_transcription_config": {
                        "enable_speaker_diarization": True,
                        "diarization_speaker_count": 0,  # Allows API to decide the number of speakers
                        "language_code": "en-US"
                    }
                }
            }
        )
        logging.info("Processing video for complaint detection...")
        result = operation.result(timeout=600)

        # Extract relevant information from the response
        annotations = []
        for annotation in result.annotation_results:
            labels = annotation.segment_label_annotations
            transcriptions = annotation.speech_transcriptions

            # Filter labels and transcriptions
            for label in labels:
                annotations.append({
                    "label": label.entity.description,
                    "confidence": label.segments[0].confidence
                })

            for transcription in transcriptions:
                for alternative in transcription.alternatives:
                    annotations.append({
                        "transcript": alternative.transcript,
                        "confidence": alternative.confidence,
                        "speakers": [{
                            "speaker_tag": word_info.speaker_tag,
                            "word": word_info.word
                        } for word_info in alternative.words]
                    })

        logging.info(f"Video analysis completed with annotations: {annotations}")
        return annotations

    except Exception as e:
        logging.error(f"Error during video processing: {e}")
        if hasattr(e, 'response'):
            logging.error(f"Error response: {e.response.content}")
        raise

def analyze_complaint(annotations):
    """
    Analyzes video annotations to determine if there is a complaint,
    uses AI to categorize the complaint into product and sub-product categories,
    and generates a summary.
    """
    complaint_keywords = ["complaint", "problem", "issue", "dissatisfied", "bad", "poor", "broken"]

    # Initialize variables
    complaint_detected = False
    combined_transcript = ""

    # Analyze labels and transcriptions
    for annotation in annotations:
        if 'label' in annotation:
            label_text = annotation['label'].lower()
            if any(keyword in label_text for keyword in complaint_keywords):
                complaint_detected = True

        if 'transcript' in annotation:
            transcript_text = annotation['transcript'].lower()
            combined_transcript += transcript_text + " "

            if any(keyword in transcript_text for keyword in complaint_keywords):
                complaint_detected = True

    # Combine all relevant text for AI classification
    combined_text = combined_transcript + " " + " ".join([annotation['label'] for annotation in annotations if 'label' in annotation])

    # Use AI to classify the product and sub-product categories
    if complaint_detected:
        classification_result = classifyProductandSummarize(combined_text)
        if isinstance(classification_result, str):
            classification_result = json.loads(classification_result)
        product = classification_result.get("product", "Unknown")
        sub_product = classification_result.get("subProduct", "Unknown")
        summary = classification_result.get("summary", "No summary available")
    else:
        summary = "No complaint detected."
        product = "Unknown"
        sub_product = "Unknown"

    return {
        "isComplaint": complaint_detected,
        "summary": summary,
        "product": product,
        "subProduct": sub_product,
        "entryText": combined_transcript  # Return the full transcribed text
    }
