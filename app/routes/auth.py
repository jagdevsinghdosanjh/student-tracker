# app/routes/auth.py

import jwt
import datetime
from flask import Blueprint, request, jsonify, render_template
from app import mongo
import os
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# 🔐 Login API (POST)
@auth_bp.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


# 🧭 Login Page (GET)
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
