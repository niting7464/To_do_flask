from flask import jsonify, request, Blueprint
from models.task import Task, db
from flask_jwt_extended import jwt_required , get_jwt_identity

task_bp = Blueprint("tasks", __name__)

# Get all tasks
@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    curr_tasks = Task.query.filter_by(user_id = current_user_id).all()
    return jsonify([{"id": t.id, "content": t.content, "complete": t.complete , "created_at" : t.created_at , "user_id" : t.user_id} for t in curr_tasks])

# Add a task
@task_bp.route("/add", methods=["POST"])
@jwt_required()
def add_task():
    data = request.get_json()
    
    content = data.get("content")
    
    user_id = get_jwt_identity()

    if not content:
        return jsonify({"error": "Task content is required"}), 400
    
    # Check if user exists
    from models.user import User
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Find the highest user_task_id for the logged-in user
    last_task = Task.query.filter_by(user_id=user_id).order_by(Task.user_task_id.desc()).first()
    new_user_task_id = (last_task.user_task_id + 1) if last_task else 1

    # Create new task
    new_task = Task(content=content, user_id=user_id , user_task_id=new_user_task_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Task added successfully",
        "task": {"id": new_task.user_task_id, "content": new_task.content}
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
