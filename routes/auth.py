from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User, db 
from models.task import Task
from flask_jwt_extended import create_access_token ,get_jwt_identity , jwt_required


auth_bp = Blueprint("auth", __name__)

# Register user
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    existing_user = User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first()
    if existing_user:
        return jsonify({"error": "User with this email or username already exists!"}), 400

    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], email=data["email"], password_hash=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500  

# Login user
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password_hash, data["password"]):

        access_token = create_access_token(identity = str(user.id))
        return jsonify({"message": "Login successful!" , "access_token" : access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    

# List of users 

@auth_bp.route("/users" , methods = ["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id" : user.id , "username" : user.username , "email" : user.email , "created_at" : user.created_at} for user in users])


# Delete user 
@auth_bp.route("/delete" , methods = ["DELETE"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error" : "User not Found"}) , 404
    
    
    Task.query.filter_by(user_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message" : "User deleted successfully!"}) , 200
        
    

