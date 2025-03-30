from models import db, User, Task
from app import app  
with app.app_context():  # Ensure database operations work inside the app context
    print("Deleting all tasks...")
    db.session.query(Task).delete()  

    print("Deleting all users...")
    db.session.query(User).delete()  

    db.session.commit() 
    print("Database reset successful! 🎯")
