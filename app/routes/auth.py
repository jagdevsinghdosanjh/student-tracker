import jwt
import datetime
from flask import Blueprint, request, jsonify
from app import mongo

auth_bp = Blueprint('auth', __name__)
SECRET_KEY="d10952582a68ffc37c05a283d1715aedd5d1890256f73475d8b5972bd6d10608"

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})
