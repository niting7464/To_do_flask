from flask import jsonify, request, Blueprint
from models.task import Task, db
from flask_jwt_extended import jwt_required , get_jwt_identity
import os
from werkzeug.utils import secure_filename
from flask import current_app


task_bp = Blueprint("tasks", __name__)

# Helper function to validate file extensions 
def allowed_file(filename):
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


# Get all tasks
@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.user_task_id).all()
    return jsonify([
        {
            "id": t.user_task_id,
            "content": t.content,
            "description": t.description,
            "complete": t.complete,
            "created_at": t.created_at,
            "files": [f.filename for f in t.files]
        }
        for t in tasks
    ])


# Add a task
@task_bp.route("/add", methods=["POST"])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()

    content = request.form.get("content")
    description = request.form.get("description")

    if not content:
        return jsonify({"error": "Task content is required"}), 400

    from models.user import User
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    last_task = Task.query.filter_by(user_id=user_id).order_by(Task.user_task_id.desc()).first()
    next_user_task_id = (last_task.user_task_id if last_task else 0) + 1

    new_task = Task(
        content=content,
        description=description,
        user_id=user_id,
        user_task_id=next_user_task_id
    )
    db.session.add(new_task)
    db.session.flush()  # So we get new_task.id before commit

    # Handle multiple files (if any)
    if "files" in request.files:
        files = request.files.getlist("files")
        from models.task import TaskFile

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                db.session.add(TaskFile(
                    filename=filename,
                    mimetype=file.mimetype,
                    task_id=new_task.id
                ))
            else:
                return jsonify({"error": "Invalid file type"}), 400

    db.session.commit()

    return jsonify({
        "message": "Task added successfully",
        "task": {
            "id": new_task.user_task_id,
            "content": new_task.content,
            "description": new_task.description,
            "files": [f.filename for f in new_task.files]
        }
    }), 201




# Delete a task
@task_bp.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):

    print(get_jwt_identity())
    current_user_id = get_jwt_identity()   
    task = Task.query.get_or_404(id)

    # Ensure only the task owner can delete it
    
    print(task.user.id)
    if task.user_id != int(current_user_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}) , 200
