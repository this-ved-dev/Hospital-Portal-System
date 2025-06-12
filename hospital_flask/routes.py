import secrets, os
from hospital_flask import app, db
from hospital_flask.models import User, Userpatient, Blog, Appointment
from hospital_flask.forms import RegistrationForm, RegisterPatientForm, LoginForm, UpdateAccountForm, UpdatePatientAccountForm, BlogForm, AddAppointment, DocEditAppointment
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user

#REGISTER USER AS DOCTOR
@app.route('/register', methods=['POST', 'GET'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        user = User(username=rform.username.data, email=rform.email.data, password=rform.password.data,
                    occupation=rform.occupation.data, specialisation=rform.specialisation.data, gender=rform.gender.data, phone=rform.phone.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login', name=rform.username.data))
    return render_template('register.html', title=' Doctor Sign Up', form=rform)


#REGISTER USER AS PATIENT
@app.route('/registerpatient', methods=['GET','POST'])
def registerpatient():
    rpform = RegisterPatientForm()
    if rpform.validate_on_submit():
        patient = Userpatient(username=rpform.username.data, email=rpform.email.data, password=rpform.password.data,
            age=rpform.age.data,gender=rpform.gender.data, phone=rpform.phone.data, image_file=rpform.image_file.data)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('login', name=rpform.username.data))
    return render_template('registerpatient.html', title='Patient Sign Up', form=rpform)


# COMMON LOGIN FORM
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(email=lform.email.data).first()
        patient = Userpatient.query.filter_by(email=lform.email.data).first()
        if patient and patient.password == lform.password.data:
            login_user(patient)
            return redirect(url_for('blog'))
        elif user and user.password == lform.password.data:
            login_user(user)
            return redirect(url_for('blog'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=lform)


# LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# MAIN BLOG
@app.route('/blog')
def blog():
    if current_user.is_authenticated:
        blog=Blog.query.all()
        return render_template('blog.html', title='All Blogs', blog=blog)
    else:
        return redirect(url_for('login'))

# ADDING A BLOG
@app.route('/blog/add', methods=['POST','GET'])
def add_blog():
    if current_user.is_authenticated:
        bform = BlogForm()
        if bform.validate_on_submit():
            blog = Blog(title=bform.title.data,content=bform.content.data,author=current_user)
            db.session.add(blog)
            db.session.commit()
            flash('Your blog has been created !!')
            return redirect(url_for('blog'))


        return render_template('addblog.html', title='Add Blog', form=bform)
    else:
        return redirect(url_for('login'))

# EDITING A BLOG
@app.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def blog_edit(blog_id):
    if current_user.is_authenticated:
        blog = Blog.query.get_or_404(blog_id)
        if blog.author != current_user:
            abort(403)
        eform = BlogForm()
        if eform.validate_on_submit():
            blog.title = eform.title.data
            blog.content = eform.content.data
            db.session.commit()
            return redirect(url_for('blog'))
        elif request.method == 'GET':
            eform.title.data = blog.title
            eform.content.data = blog.content
        return render_template('editblog.html', title='Edit Blog', form=eform, blog=blog)
    else:
        return redirect(url_for('login'))

# DELETING A BLOG
@app.route('/blog/<int:blog_id>/delete', methods=['POST'])
def blog_delete(blog_id):
    if current_user.is_authenticated:
        blog = Blog.query.get_or_404(blog_id)
        if blog.author != current_user:
            abort(403)
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for('blog'))
    else:
        return redirect(url_for('login'))


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_name)
    form_image.save(image_path)
    return image_name
# PROFILE PAGE
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        if current_user.user_type == 'doctor':
            uform = UpdateAccountForm()
            if uform.validate_on_submit():
                if uform.image_file.data:
                    uform.image_file.data = save_image(uform.image_file.data)
                    current_user.image_file = uform.image_file.data
                current_user.username = uform.username.data
                current_user.email = uform.email.data
                current_user.phone = uform.phone.data
                current_user.occupation = uform.occupation.data
                current_user.specialisation = uform.specialisation.data
                current_user.gender = uform.gender.data
                
                db.session.commit()
                return redirect(url_for('profile'))
            elif request.method == 'GET':
                uform.username.data = current_user.username
                uform.email.data = current_user.email
                uform.phone.data = current_user.phone
                uform.occupation.data = current_user.occupation
                uform.specialisation.data = current_user.specialisation
                uform.gender.data = current_user.gender
            image_file = url_for(
                'static', filename='profile_pics/' + current_user.image_file)
            return render_template('profile.html', title='Profile', image_file=image_file, form=uform)
        elif current_user.user_type == 'patient':
            upform = UpdatePatientAccountForm()
            if upform.validate_on_submit():
                if upform.image_file.data:
                    upform.image_file.data = save_image(upform.image_file.data)
                    current_user.image_file = upform.image_file.data
                current_user.username = upform.username.data
                current_user.email = upform.email.data
                current_user.phone = upform.phone.data
                current_user.age = upform.age.data
                current_user.gender = upform.gender.data

                db.session.commit()
                return redirect(url_for('profile'))
            elif request.method == 'GET':
                upform.username.data = current_user.username
                upform.email.data = current_user.email
                upform.phone.data = current_user.phone
                upform.age.data = current_user.age
                upform.gender.data = current_user.gender
            image_file = url_for(
                'static', filename='profile_pics/' + current_user.image_file)

            return render_template('profile.html', title='Profile', image_file=image_file, form=upform)
    else:
        return redirect(url_for('login'))


#APPOINTMENT
@app.route('/appointment')
def appointment():
    if current_user.is_authenticated:
        appointment = Appointment.query.all()
        return render_template('appointment.html', title='All Appointments',appointment=appointment)
    

@app.route('/appointment/add', methods=['GET', 'POST'])
def add_appointment():
    if current_user.is_authenticated:
        aaform = AddAppointment();
        if aaform.validate_on_submit():
            appointment = Appointment(doctor=User.query.filter_by(username=aaform.doctor_name.data).first(), symptom=aaform.symptom.data, patient=current_user)
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('appointment'))
        return render_template('addappointment.html',title='Add Appointment',form=aaform)
    else:
        return redirect(url_for('login'))
#STAFF
@app.route('/staff')
def staff():
    if current_user.is_authenticated:
        staff = User.query.all()
        return render_template('staff.html', title='Staff', staff=staff)

    else:
        return redirect(url_for('login'))

#EDITING APPOINTMENT PATIENTS SIDE
@app.route('/appointment/<int:appointment_id>', methods=['GET', 'POST'])
def patient_edit(appointment_id):
    if current_user.is_authenticated:
        appointment = Appointment.query.get_or_404(appointment_id)
        if appointment.patient != current_user:
            abort(403)
        epaform = AddAppointment()
        if epaform.validate_on_submit():
            doctorname = User.query.filter_by(username=epaform.doctor_name.data).first()            
            appointment.doctor_id = doctorname.id
            appointment.symptom = epaform.symptom.data
            db.session.commit()
            return redirect(url_for('appointment'))
        elif request.method == 'GET':
            epaform.doctor_name.data = appointment.doctor.username
            epaform.symptom.data = appointment.symptom
        return render_template('editappointment.html', title='Edit Appointment', form=epaform, appointment=appointment)
    else:
        return redirect(url_for('login'))


#DELETING APPOINTMENT PATIENTS SIDE
@app.route('/appointment/<int:appointment_id>/delete', methods=['POST'])
def patient_delete(appointment_id):
    if current_user.is_authenticated:
        appointment = Appointment.query.get_or_404(appointment_id)
        if appointment.patient != current_user:
            abort(403)
        db.session.delete(appointment)
        db.session.commit()
        return redirect(url_for('appointment'))
    else:
        return redirect(url_for('login'))


#EDITING APPOINTMENT DOCTORS SIDE
@app.route('/appointment/doctor-<int:appointment_id>', methods=['GET', 'POST'])
def doctor_edit(appointment_id):
    if current_user.is_authenticated:
        appointment = Appointment.query.get_or_404(appointment_id)
        if appointment.doctor != current_user:
            abort(403)
        edaform = DocEditAppointment()
        if edaform.validate_on_submit():
            appointment.status = edaform.status.data
            appointment.diagnosis = edaform.diagnosis.data
            db.session.commit()
            return redirect(url_for('appointment'))
        elif request.method == 'GET':
            edaform.status.data = appointment.status
            edaform.diagnosis.data = appointment.diagnosis
        return render_template('editappointment.html', title='Edit Appointment', form=edaform, appointment=appointment)
    else:
        return redirect(url_for('login'))







@app.route('/department')
def department():
    if current_user.is_authenticated:
        return render_template('department.html', title='Our Departments')
