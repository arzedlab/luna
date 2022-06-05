from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(24))
    password = db.Column(db.String(256))
    name = db.Column(db.String(1000))

    def __init__(self, email, role, password, name, username) -> None:
        self.email = email
        self.role = role
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.name = name

    def __repr__(self) -> str:
        return f"<Name: {self.name}, Email: {self.email}, Role: {self.role} >"