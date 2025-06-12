from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FileField, TextAreaField
from flask_wtf.file import FileAllowed
from wtforms import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from hospital_flask.models import User, Userpatient, Blog
from flask_login import current_user

# FORM TO REGISTER A DOCTOR


class RegistrationForm(FlaskForm):
    username = StringField('Full Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    occupation = StringField('Occupation', validators=[DataRequired()])
    specialisation = StringField('Specialisation', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
                         ('Male'), ('Female')], validators=[DataRequired()])
    phone = StringField('Phone No.', validators=[
                        DataRequired(), Length(min=10, max=10)])
    image_file = FileField('Profile Pic', validators=[
                           FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Create Account')

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Account with this email exists !')

# FORM TO REGISTER A PATIENT


class RegisterPatientForm(FlaskForm):
    username = StringField('Full Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    phone = StringField('Phone No.', validators=[
                        DataRequired(), Length(min=10, max=10)])
    age = StringField('Age', validators=[
                      NumberRange(min=0, max=None), DataRequired()])
    gender = SelectField('Gender', choices=[
                         ('Male'), ('Female')], validators=[DataRequired()])
    image_file = FileField('Profile Pic', validators=[
                           FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Add Patient')

    def validate_email(self, email):
        email = Userpatient.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Account with this email exists !')

# FORM TO LOGIN AS DOCTOR OR USER


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    submit = SubmitField('Log-In')

# FORM TO UPDATE DOCTOR PROFILE


class UpdateAccountForm(FlaskForm):
    username = StringField('Full Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    occupation = StringField('Occupation', validators=[DataRequired()])
    specialisation = StringField('Specialisation', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
                         ('Male'), ('Female')], validators=[DataRequired()])
    phone = StringField('Phone No.', validators=[
                        DataRequired(), Length(min=10, max=10)])
    image_file = FileField('Profile Pic', validators=[
                           FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Account with this email exists !')


# FORM TO UPDATE PATIENT PROFILE
class UpdatePatientAccountForm(FlaskForm):
    username = StringField('Full Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[
                       NumberRange(min=0, max=None), DataRequired()])
    gender = SelectField('Gender', choices=[
                         ('Male'), ('Female')], validators=[DataRequired()])
    phone = StringField('Phone No.', validators=[
                        DataRequired(), Length(min=10, max=10)])
    image_file = FileField('Profile Pic', validators=[
                           FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Account with this email exists !')


# FORM TO CREATE AND EDIT A BLOG
class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Blog')


# FORM TO ADD/EDIT APPOINTMENT BY PATIENT
class AddAppointment(FlaskForm):
    doctor_name = StringField('Doctor Name', validators=[DataRequired()])
    symptom = TextAreaField('Symptom', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')

# FORM TO EDIT APPOINTMENT BY DOCTOR


class DocEditAppointment(FlaskForm):
    status = SelectField('Status', choices=[
                         ('CONSULTATION'), ('ON-GOING'), ('TREATED')], validators=[DataRequired()])
    diagnosis = TextAreaField('Symptom', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')
