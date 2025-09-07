
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# Demo credentials (replace with real user store if needed)
DEMO_USER = {"username": "admin", "password": "admin123"}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if username == DEMO_USER["username"] and password == DEMO_USER["password"]:
        token = create_access_token(identity=username)
        return jsonify({"access_token": token})
    return jsonify({"error": "invalid credentials"}), 401
