from venv import logger
from flask import Blueprint, jsonify, request
from elasticsearch import Elasticsearch, helpers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Entry, User
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Create a Blueprint for Elasticsearch routes
elastic_bp = Blueprint('elastic_bp', __name__)

# Initialize Elasticsearch client
client = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL"),
    api_key=os.getenv("ELASTICSEARCH_API_KEY")
)

# Initialize SQLAlchemy session
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def generate_actions(entries):
    for entry in entries:
        yield {
            "_index": "postgres1", 
            "_id": entry.id,  # Primary key as the document ID
            "_source": {
                "entryId": entry.entryId,
                "isComplaint": entry.isComplaint,
                "product": entry.product,
                "subProduct": entry.subProduct,
                "entryText": entry.entryText,
                "summary": entry.summary,
                "fileType": entry.fileType.value,  # Assuming Elasticsearch can index enum as a string
                "userId": entry.userId,
            }
        }

@elastic_bp.route('/elastic/sync', methods=['POST'])
def sync_data():
    try:
        # Fetch all records from the database
        records = session.query(Entry).all()

        # Prepare bulk indexing actions
        actions = generate_actions(records)
        
        # Capture successes, failures, and responses
        success, failed = 0, 0
        error_responses = []

        # Perform bulk indexing with detailed logging
        for ok, response in helpers.streaming_bulk(client, actions):
            if not ok:
                failed += 1
                error_responses.append(response)
            else:
                success += 1

        if failed > 0:
            # Log error responses for failed documents
            print(f"Failed Documents: {error_responses}")
            return jsonify({"error": f"{failed} document(s) failed to index.", "details": error_responses}), 500
        else:
            return jsonify({"status": f"sync completed, {success} documents indexed"})
    except Exception as e:
        # Log the exception details
        print(f"Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

@elastic_bp.route('/elastic/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '')  # Get search query from request
        is_complaint = request.args.get('isComplaint', None)  # Filter by complaint status

        # Log the incoming query parameters
        logger.info(f"Search Request - query: {query}, isComplaint: {is_complaint}")

        es_query = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "entryId", "product", "subProduct", "entryText", "summary"
                            ]
                        }
                    },
                    "filter": []
                }
            }
        }
        
        if is_complaint is not None:
            es_query['query']['bool']['filter'].append({
                "term": {"isComplaint": is_complaint.lower() == 'true'}
            })

        # Log the Elasticsearch query
        logger.info(f"Elasticsearch Query: {es_query}")

        response = client.search(index="postgres1", body=es_query)

        # Log the response from Elasticsearch
        logger.info(f"Elasticsearch Response: {response}")

        return jsonify(response['hits']['hits'])
    except Exception as e:
        # Log the exception details
        logger.exception(f"Exception during search: {str(e)}")
        return jsonify({"error": str(e)}), 500
