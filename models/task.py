from datetime import datetime
from models import db  # Import shared db instance

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) # global id
    user_task_id = db.Column(db.Integer, nullable=False)  # User-specific ID
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key - links to User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'user_task_id', name='user_task_uc'),
    )

