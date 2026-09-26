from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from auth_database import (
    create_user,
    get_user_by_email,
    get_all_users,
    update_user_role
)


# =========================================================
# AUTH BLUEPRINT
# =========================================================

auth_bp = Blueprint("auth", __name__)


# =========================================================
# ROLE PROTECTION
# =========================================================

def role_required(*allowed_roles):

    def decorator(function):

        from functools import wraps

        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):

            claims = get_jwt()

            user_role = claims.get("role")

            if user_role not in allowed_roles:

                return jsonify({
                    "success": False,
                    "message": "Access denied."
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


# =========================================================
# SIGNUP
# =========================================================

@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not name or not email or not password:

        return jsonify({
            "success": False,
            "message": "Name, email and password are required."
        }), 400

    if len(password) < 6:

        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    existing_user = get_user_by_email(email)

    if existing_user:

        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    password_hash = generate_password_hash(password)

    # Allow selecting doctor or staff on signup (protect admin from direct signup)
    requested_role = data.get("role", "doctor").strip().lower()
    if requested_role not in ["doctor", "staff"]:
        requested_role = "doctor"
    role = requested_role

    try:

        user_id = create_user(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role
        )

        return jsonify({
            "success": True,
            "message": "Account created successfully.",
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "role": role
            }
        }), 201

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    user = get_user_by_email(email)

    if not user:

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    if not check_password_hash(
        user["password_hash"],
        password
    ):

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "role": user["role"],
            "name": user["name"],
            "email": user["email"]
        }
    )

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "token": access_token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


# =========================================================
# CURRENT USER
# =========================================================

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def current_user():

    claims = get_jwt()

    return jsonify({
        "success": True,
        "user": {
            "name": claims.get("name"),
            "email": claims.get("email"),
            "role": claims.get("role")
        }
    }), 200


# =========================================================
# ADMIN - GET ALL USERS
# =========================================================

@auth_bp.route("/users", methods=["GET"])
@role_required("admin")
def get_users():

    users = get_all_users()

    return jsonify({
        "success": True,
        "users": [
            {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "created_at": user["created_at"]
            }
            for user in users
        ]
    }), 200


# =========================================================
# ADMIN - CHANGE USER ROLE
# =========================================================

@auth_bp.route(
    "/users/<int:user_id>/role",
    methods=["PUT"]
)
@role_required("admin")
def change_user_role(user_id):

    data = request.get_json() or {}

    new_role = data.get(
        "role",
        ""
    ).strip().lower()

    # Admin cannot create another admin through this API.
    if new_role not in ["doctor", "staff"]:

        return jsonify({
            "success": False,
            "message": "Role must be doctor or staff."
        }), 400

    updated_user = update_user_role(
        user_id,
        new_role
    )

    if not updated_user:

        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "User role updated successfully.",
        "user": {
            "id": updated_user["id"],
            "name": updated_user["name"],
            "email": updated_user["email"],
            "role": updated_user["role"],
            "created_at": updated_user["created_at"]
        }
    }), 200