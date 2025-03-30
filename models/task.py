from datetime import datetime
from models import db  # Import shared db instance

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key - links to User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

