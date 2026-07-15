from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudentModel(db.Model):
    __tablename__ = "students"

    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name  = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    gender     = db.Column(db.String(20), nullable=False)
    hobbies    = db.Column(db.String(300))
    country    = db.Column(db.String(60), nullable=False)

    def __init__(self, first_name, second_name, email, password, gender, hobbies, country):
        self.first_name = first_name
        self.last_name  = second_name
        self.email      = email
        self.password   = password
        self.gender     = gender
        self.hobbies    = hobbies
        self.country    = country

    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"