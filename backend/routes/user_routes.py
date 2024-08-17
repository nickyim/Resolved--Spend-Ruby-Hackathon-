from flask import Blueprint, request, jsonify
from model import db, User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    clerk_id = data.get('clerkId')
    email = data.get('email')

    if not clerk_id or not email:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(clerkId=clerk_id).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"error": "Email already exists"}), 400
    
    # Create new user
    new_user = User(clerkId=clerk_id, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/user', methods=['GET'])
def get_user():
    clerk_id = request.args.get('clerkId')

    if not clerk_id:
        return jsonify({"error": "No clerkId provided"}), 400

    user = User.query.filter_by(clerkId=clerk_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "clerkId": user.clerkId,
        "email": user.email
    })
