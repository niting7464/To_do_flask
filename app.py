from flask import Flask, jsonify , request 
from flask_jwt_extended import JWTManager, jwt_required
from models import db 
from routes.auth import auth_bp
from routes.tasks import task_bp
from routes.admin_routes import admin_bp
from extensions import jwt
from flask_migrate import Migrate
from datetime import timedelta
import os 
import cloudinary
import cloudinary.uploader



app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "MUMMA"
app.config['JWT_HEADER_TYPE'] = ''     # to remove bearer in front for authoriztion  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt.init_app(app)

# ✅ Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/to_do_flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'txt', 'docx'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Cloudinary
cloudinary.config(
  cloud_name = 'dqcylcdoa',
  api_key = '542728284488218',
  api_secret = '7d1js_Vsween4hKvZHf0ZXirAlg',
  secure = True
)



# ✅ Initialize Database
db.init_app(app)
migrate = Migrate(app, db)


# ✅ Create Tables
with app.app_context():
    db.create_all()
    

# ✅ Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(task_bp, url_prefix="/tasks")
app.register_blueprint(admin_bp, url_prefix="/admin")


@app.route("/")
def home():
    return jsonify({"message": "Welcome to Flask API"})

if __name__ == "__main__":
    app.run(debug=True)
