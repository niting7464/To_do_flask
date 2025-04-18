from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so they are registered with SQLAlchemy
from .user import User
from .role import Role
from .permission import Permission
from .rbac_associations import user_roles, roles_permissions


