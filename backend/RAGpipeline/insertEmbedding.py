import json
from dotenv import load_dotenv
from pinecone import Pinecone
import os
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings(api_key=openai_api_key)
embed_model = "text-embedding-3-small"

pc = Pinecone(api_key=pinecone_api_key)
pinecone_index = pc.Index("rubyhackcomplaints")

# Load JSON file
with open('RAGpipeline/hugeComplaintsJson.json', 'r') as file:
    data = json.load(file)

# Iterate over each JSON object
for obj in data:
    # Extract relevant text fields
    # Extract and concatenate relevant text fields
    source = obj['_source']
    text = f"""
    Index: {obj.get('_index', '')}
    Type: {obj.get('_type', '')}
    ID: {obj.get('_id', '')}
    SORT: {obj.get('sort', '')}
    Score: {obj.get('_score', '')}
    Product: {source.get('product', '')}
    Complaint: {source.get('complaint_what_happened', '')}
    Date Sent to Company: {source.get('date_sent_to_company', '')}
    Issue: {source.get('issue', '')}
    Sub Product: {source.get('sub_product', '')}
    Zip Code: {source.get('zip_code', '')}
    Tags: {source.get('tags', '')}
    Complaint ID: {source.get('complaint_id', '')}
    Timely: {source.get('timely', '')}
    Consumer Consent Provided: {source.get('consumer_consent_provided', '')}
    Company Response: {source.get('company_response', '')}
    Submitted Via: {source.get('submitted_via', '')}
    Company: {source.get('company', '')}
    Date Received: {source.get('date_received', '')}
    State: {source.get('state', '')}
    Consumer Disputed: {source.get('consumer_disputed', '')}
    Company Public Response: {source.get('company_public_response', '')}
    Sub Issue: {source.get('sub_issue', '')}
    """
    
    # Generate embedding
    embedding = embeddings.embed_query(text)
    
    # Upload embedding to Pinecone
    pinecone_index.upsert([(obj['_id'], embedding)], namespace='complaints')