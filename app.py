from flask import Flask, jsonify , request 
from flask_jwt_extended import JWTManager
from models import db 
from routes.auth import auth_bp
from routes.tasks import task_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "MUMMA"

app.config['JWT_HEADER_TYPE'] = ''      # to remove bearer in front for authoriztion 
jwt = JWTManager(app) 

# ✅ Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize Database
db.init_app(app)

# ✅ Create Tables
with app.app_context():
    db.create_all()

# ✅ Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(task_bp, url_prefix="/tasks")

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Flask API"})

if __name__ == "__main__":
    app.run(debug=True)
