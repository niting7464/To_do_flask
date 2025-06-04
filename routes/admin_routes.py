# routes/admin_routes.py or wherever appropriate
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Role, db
from decorators import admin_required  # optional, to restrict access

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/assign-role', methods=['POST'])
@jwt_required()
@admin_required  # Only allow admins to assign roles

def assign_role():
    data = request.get_json()
    user_email = data.get("email")
    role_name = data.get("role")

    if not user_email or not role_name:
        return jsonify({"message": "Email and role are required"}), 400

    user = User.query.filter_by(email=user_email).first()
    role = Role.query.filter_by(name=role_name).first()

    if not user:
        return jsonify({"message": f"User with email {user_email} not found"}), 404
    if not role:
        return jsonify({"message": f"Role {role_name} not found"}), 404

    if role in user.roles:
        return jsonify({"message": f"User already has role '{role_name}'"}), 200

    user.roles.append(role)
    db.session.commit()
    return jsonify({"message": f"Assigned role '{role_name}' to user '{user_email}'"}), 200
