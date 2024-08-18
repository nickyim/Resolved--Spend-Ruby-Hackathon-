from flask import Blueprint, request, jsonify
from model import db, User, Entry
import logging

dashboard_bp = Blueprint('dashboard_bp', __name__)

logging.basicConfig(level=logging.INFO)

@dashboard_bp.route('/getDashboard', methods=['GET', 'OPTIONS'])
def get_dashboard():
    if request.method == 'OPTIONS':
        return jsonify({}), 200 

    # Extract clerkId from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Invalid or missing Authorization header"}), 401

    clerk_id = auth_header.split(' ')[1]
    logging.info(f"Extracted clerkId: {clerk_id}")

    # Fetch the user from the database
    user = User.query.filter_by(clerkId=clerk_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    logging.info(f"Found user: {user.email} with admin status: {user.is_admin}")

    # Fetch entries based on user's admin status
    if user.is_admin:
        entries = Entry.query.all()  # Admins see all entries
    else:
        entries = Entry.query.filter_by(userId=user.id).all()  # Regular users see only their entries

    result = []
    for entry in entries:
        result.append({
            "id": entry.id,
            "entryId": entry.entryId,
            "isComplaint": entry.isComplaint,
            "product": entry.product,
            "subProduct": entry.subProduct,
            "entryText": entry.entryText,
            "summary": entry.summary,
            "fileType": entry.fileType.name,  # Convert Enum to string
            "created_at": entry.created_at.isoformat(),
        })

    return jsonify(result), 200
