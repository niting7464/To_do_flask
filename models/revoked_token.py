from models import db

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)  # JWT Token ID
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
