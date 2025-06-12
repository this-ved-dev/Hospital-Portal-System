from hospital_flask import db, login_manager
from datetime import datetime
from flask_login import UserMixin
# login manager has 4 paarameters 1. is authenticated 2.isactive 3.isanonymous 4. getId
@login_manager.user_loader
def load_user(user_email):
    return Userpatient.query.filter_by(email=user_email).first() or User.query.filter_by(email=user_email).first()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    occupation = db.Column(db.String(20),nullable=False)
    specialisation = db.Column(db.String(60),nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    user_type = db.Column(db.String,nullable=False, default='doctor')
    image_file = db.Column(db.String(20), nullable=False,
                           default='auto.jpg')
   
    blog = db.relationship('Blog', backref='author', lazy=True)
    appointment = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def get_id(self):
        return str(self.email)

class Userpatient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.String, nullable=False, default='patient')
    image_file = db.Column(db.String(20), nullable=False, default='auto.jpg')

    appointment = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        return f"Userpatient('{self.username}','{self.email}','{self.image_file}')"

    def get_id(self):
        return str(self.email)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Blog('{self.title}','{self.date_posted}')"


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('userpatient.id'), nullable=False)
    date_appointed = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10),nullable=False, default='CONSULTATION')
    symptom = db.Column(db.String(100), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False, default='TO BE FILLED BY DOCTOR')
    