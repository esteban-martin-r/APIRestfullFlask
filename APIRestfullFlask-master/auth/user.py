from app import app, db
from models import User

with app.app_context():
    user = User(username="esteban")
    user.password = "123456"  
    db.session.add(user)
    db.session.commit()
    print("Usuario creado:", user.username)