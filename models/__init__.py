from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so they are registered with SQLAlchemy
from .user import User
from .task import Task
from .role import Role
from .permission import Permission
from .rbac_associations import user_roles, roles_permissions
from .task import TaskFile
from .revoked_token import RevokedToken

# optional if you want to expose them
__all__ = [
    "db",
    "User",
    "Task",
    "Role",
    "Permission",
    "user_roles",
    "roles_permissions",
    "TaskFile",
    "RevokedToken"
]


