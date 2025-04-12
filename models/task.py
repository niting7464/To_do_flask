from models import db  # Import shared db instance
from datetime import datetime

# Define TaskFile model first so Task can reference it in relationship
class TaskFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # original or stored filename
    mimetype = db.Column(db.String(100))  # for file type (image/jpeg, video/mp4 etc.)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # global id
    user_task_id = db.Column(db.Integer, nullable=False)  # User-specific ID
    content = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key - links to User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    files = db.relationship('TaskFile', backref='task', lazy=True)  # ✅ Link to TaskFile

    __table_args__ = (
        db.UniqueConstraint('user_id', 'user_task_id', name='user_task_uc'),
    )
