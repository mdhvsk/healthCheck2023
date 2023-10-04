from time import time
from flask import Flask, session, render_template, redirect, request, flash
from flask_app import app
from flask_app.model.model_patient import Patient
from flask_app.model.model_medication import Medication
from flask_app.model.model_appointment import Appointment
from flask_app.model.model_vitals import BloodPressure, BloodSugar, HeartRate
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/patientVerificationForm', methods=["POST"])
def patientVerificationForm():
    return redirect('/verification')


@app.route('/signUpForm', methods=['POST'])
def signUpForm():
    print("Signed in")
    answer = Patient.validateSignInForm(request.form)
    if answer == False:
        return redirect('/signUpPage')
    hashedPassword = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashedPassword
    }

    id = Patient.registerUser(data)
    print(id)
    user_in_db = Patient.getUserByEmail(request.form)
    session['id'] = user_in_db['id']
    session['email'] = user_in_db['email']
    session['first_name'] = user_in_db['first_name']
    session['last_name'] = user_in_db['last_name']
    session['loggedIn'] = True

    return redirect('/dashboardPage')


@app.route('/loginForm', methods=['POST'])
def loginForm():
    print("logged in ")
    user_in_db = Patient.getUserByEmail(request.form)
    if user_in_db == False:
        flash("Invalid Email/Password", 'login')
        return redirect("/loginPage")

    if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    session['id'] = user_in_db['id']
    session['email'] = user_in_db['email']
    session['first_name'] = user_in_db['first_name']
    session['last_name'] = user_in_db['last_name']
    session['loggedIn'] = True
    return redirect('/dashboardPage')


@app.route('/logoutForm', methods=['POST'])
def logoutForm():
    print("logged out ")
    session.clear()
    return redirect('/')


# ******************* LOGIN/LOGOUT END *******************
