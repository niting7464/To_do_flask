from models.rbac_associations import roles_permissions
from models.permission import Permission
from models import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    permissions = db.relationship('Permission', secondary=roles_permissions, backref='roles')
