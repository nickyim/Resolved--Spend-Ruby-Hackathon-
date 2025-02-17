from datetime import datetime, timezone
from model import db, User, Entry
from flask import Blueprint, json, request, jsonify
import uuid
from routes.elastic_routes import sync_data

def updateDB(file_type, text, user, result):
    # Parse the result into JSON
    result_data = json.loads(result)
    is_complaint = result_data.get('isComplaint', False)
    summary = result_data.get('summary', '')
    product = result_data.get('product', '')
    sub_product = result_data.get('subProduct', '')

    # Generate a unique entryId
    entry_id = str(uuid.uuid4())

    # Create a new entry and associate it with the user
    new_entry = Entry(
        entryId=entry_id,
        isComplaint=is_complaint,
        product=product,
        subProduct=sub_product,
        entryText=text,
        summary=summary,
        userId=user.id,
        fileType=file_type,
        created_at=datetime.now(timezone.utc)
    )

    db.session.add(new_entry)
    db.session.commit()

    # Sync the newly created entry with Elasticsearch
    try:
        sync_data()
        print("Successfully synced data with Elasticsearch")
    except Exception as e:
        print(f"Error syncing data with Elasticsearch: {e}")

    print(f"Received text result: {result_data}")

    return jsonify({
        "message": "Prompt processed and entry created successfully",
        "entryId": entry_id,
        "isComplaint": is_complaint,
        "summary": summary,
        "product": product,
        "subProduct": sub_product,
        "fileType": file_type,
        "created_at": new_entry.created_at.isoformat(),
        "user": {
            "id": user.id,
            "clerkId": user.clerkId,
            "email": user.email
        }
    }), 201
