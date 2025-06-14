from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User, db
from models.task import Task
from models.role import Role
from models.revoked_token import RevokedToken
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

import re  # For email validation

auth_bp = Blueprint("auth", __name__)


# ✅ Function to validate email format
def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)


# ✅ Register user with validations
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Check for missing fields
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Username, email, and password are required!"}), 400

    # Validate email format
    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format!"}), 400

    # Check if email or username is already taken
    existing_user = User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first()
    if existing_user:
        return jsonify({"error": "User with this email or username already exists!"}), 400

    # Validate password strength
    password = data["password"]

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long!"}), 400
    if not any(c.isdigit() for c in password):
        return jsonify({"error": "Password must contain at least one digit!"}), 400
    if not any(c.isupper() for c in password):
        return jsonify({"error": "Password must contain at least one uppercase letter!"}), 400


    # Hash password and create user
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], email=data["email"], password_hash=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500  
    

# ✅ Login user with validations
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Check for missing fields
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required!"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))  # Convert ID to string for JWT
    refresh_token = create_refresh_token(identity=str(user.id))

    # 🆕 Get user's roles
    user_roles = [role.name for role in user.roles]

    return jsonify({
        "message": "Login successful!",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "roles": user_roles    # 🆕 Return roles too!
    }), 200



# Refresh token 
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Only allow refresh tokens
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


# ✅ Logout user (Blacklist token)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Extract token ID
    revoked_token = RevokedToken(jti=jti)  # Store in DB
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify({"message": "Successfully logged out!"}), 200


# ✅ List of all users
@auth_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email, "created_at": user.created_at} for user in users])


# ✅ Delete user (Ensures user exists)
@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    Task.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


@auth_bp.route('/make-admin', methods=['POST'])
def make_admin():
    data = request.get_json()
    secret_key = data.get('secret_key')
    if secret_key != "MY_SUPER_SECRET":
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.filter_by(email=data.get("email")).first()
    admin_role = Role.query.filter_by(name="Admin").first()
    if user and admin_role:
        user.roles.append(admin_role)
        db.session.commit()
        return jsonify({"message": "User promoted to Admin!"}), 200
    else:
        return jsonify({"error": "User or Admin role not found."}), 404

