import uuid
from flask import Blueprint, json, request, jsonify
from chatScripts.parseComplaint import processComplaint
from model import db, User, Entry

text_bp = Blueprint('text_bp', __name__)

@text_bp.route('/textQuery', methods=['POST', 'OPTIONS'])
def handle_prompt():
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
    
    data = request.json 
    prompt = data.get('prompt')
    clerk_id = data.get('clerkId')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    if not clerk_id:
        return jsonify({"error": "No clerkId provided"}), 400
    
    # Fetch the user from the database
    user = User.query.filter_by(clerkId=clerk_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Process the complaint using AI
    result = processComplaint(prompt)
    
    # Parse the result into JSON (assuming it's returned as a string)
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
        entryText=prompt,
        summary=summary,
        userId=user.id
    )

    db.session.add(new_entry)
    db.session.commit()

    print(f"Received text result: {result_data}")

    return jsonify({
        "message": "Prompt processed and entry created successfully",
        "entryId": entry_id,
        "isComplaint": is_complaint,
        "summary": summary,
        "product": product,
        "subProduct": sub_product,
        "user": {
            "id": user.id,
            "clerkId": user.clerkId,
            "email": user.email
        }
    }), 201
