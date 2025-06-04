
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Check if user has 'Admin' role
        if not any(role.name == "Admin" for role in user.roles):
            return jsonify({"message": "Admin privilege required"}), 403

        return fn(*args, **kwargs)
    return wrapper
