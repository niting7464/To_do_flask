# imports
from flask import Flask, render_template, redirect, request  # Flask framework tools
from flask_scss import Scss  # Enables SCSS (but Flask-Scss is outdated)
from flask_sqlalchemy import SQLAlchemy  # ORM to handle databases
from datetime import datetime  # Handles date and time



# My App Setup
app = Flask(__name__)  # Initializes the Flask application
Scss(app)  # Enables SCSS 


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  
db = SQLAlchemy(app)  # Create an instance of SQLAlchemy


# Data class -> Row of data
class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)                # Unique identifier (Primary Key)
    content = db.Column(db.String(100), nullable=False)         # Task content (must not be empty)
    complete = db.Column(db.Integer, default=0)                 # Tracks task completion (0 = incomplete)
    created = db.Column(db.DateTime, default=datetime.utcnow)   # Auto sets timestamp when created

    def __repr__(self) -> str:
        return f"Task {self.id}"                                # Returns task ID when printed




# Routes for webpages
# Homepage
@app.route('/', methods=["POST", "GET"])
def index():


    # Add a task 
    if request.method == "POST":
        current_task = request.form['content']  # Get task content from the form
        new_task = Mytask(content=current_task)  # Create a new task object

        try:
            db.session.add(new_task)  # Add task to the database session
            db.session.commit()  # Commit changes to the database
            return redirect('/')  # Redirect to homepage
        except Exception as e:
            print(f"ERROR:{e}")  # Print error in terminal if something goes wrong
            return f"ERROR:{e}"  # Return error message to the browser


    # See all current tasks    
    else:
        tasks = Mytask.query.order_by(Mytask.created).all()       # Fetch all tasks ordered by creation date
        return render_template('index.html' , tasks = tasks)
    

    # delete an item
@app.route("/delete/<int:id>", methods=["POST"])        # Only allow POST for safety
def delete(id:int):
        delete_task = Mytask.query.get_or_404(id)       # Find the task or return 404
        try:
            db.session.delete(delete_task)           # Delete the task
            db.session.commit()               # Commit changes
            return redirect("/")              # Redirect to homepage 
        except Exception as e:
            return f"ERROR:{e}"
        










        

# Runner and Debugger
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures the database and table are created before running the app

    app.run(debug=True)  # Starts the development server with debugging enabled
