from flask import Flask, session, render_template, redirect, request, flash
from flask_app import app
from flask_app.model.model_appointment import Appointment
from flask_app.model.model_medication import Medication
from flask_app.model.model_patient import Patient
from flask_app.model.model_vitals import BloodPressure, BloodSugar, HeartRate
from datetime import datetime

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def welcomePage():
    session['loggedIn'] = False
    return render_template("welcome.html")


@app.route('/loginPageDoctor')
def loginPageDoctor():
    return render_template("/doctor/login.html")


@app.route('/verification')
def verification():
    return render_template("/patient/login_and_reg/patient_verification.html")


@app.route('/signUpPage')
def signUpPage():
    return render_template("/patient/login_and_reg/sign_up.html")


@app.route('/loginPage')
def loginPage():
    return render_template("/patient/login_and_reg/login.html")

# ************************ DASHBOARD ********************************** #


@app.route('/dashboardPage')
def dashboardPage():
    if session['loggedIn'] == False:
        return render_template('/')
    data = {
        'users_id': session['id'],
        'patient_id': session['id'],
        'user_id': session['id']

    }
    nextAppointment = Appointment.getOneAppointment(data)
    lastHeartRate = HeartRate.getLastHeartRate(data)
    lastBloodPressure = BloodPressure.getLastBP(data)
    lastBloodSugar = BloodSugar.getLastBloodSugar(data)

    medications, closestRefill, closestRefillMed = Medication.getAllMeds(data)
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    session['currentDay'] = days[datetime.today().weekday()]
    currentDay = session['currentDay']

    x = HeartRate.plotHeartRate(data)
    y = BloodPressure.plotbloodPressure(data)
    z = BloodSugar.plotbloodSugar(data)
    return render_template("patient/dashboard/dashboard.html", first_name=session['first_name'], nextAppt=nextAppointment, lastHR=lastHeartRate, lastBP=lastBloodPressure, lastBS=lastBloodSugar, meds=medications, currDay=currentDay, refill=closestRefill, upcomingMed=closestRefillMed)


# ************************ APPOINTMENTS ********************************** #
@app.route('/appointmentsPage')
def appointmentsPage():
    if session['loggedIn'] == False:
        return render_template('/')
    data = {
        'users_id': session['id']
    }
    appointments = Appointment.getAppointments(data)

    return render_template("patient/dashboard/appointments.html", appts=appointments, first_name=session['first_name'])


@app.route('/appointmentsPage/add')
def appointmentsAdd():
    if session['loggedIn'] == False:
        return render_template('/')
    return render_template("patient/dashboard/forms/appointmentsAdd.html", first_name=session['first_name'])


# ************************ Medications ********************************** #

@app.route('/medicationsPage')
def medicationsPage():
    if session['loggedIn'] == False:
        return render_template('/')
    data = {
        'user_id': session['id']
    }
    medications, closestRefill, closestRefillMed = Medication.getAllMeds(data)
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    session['currentDay'] = days[datetime.today().weekday()]
    currentDay = session['currentDay']
    print(closestRefill)
    return render_template("patient/dashboard/medications.html", meds=medications, currDay=currentDay, refill=closestRefill, first_name=session['first_name'])


@app.route('/medicationsPage/add')
def medicationsAdd():
    if session['loggedIn'] == False:
        return render_template('/')
    return render_template("patient/dashboard/forms/medicationsAdd.html", first_name=session['first_name'])


# ************************ Vitals ********************************** #

@app.route('/vitalsPage')
def vitalsPage():
    if session['loggedIn'] == False:
        return render_template('/')
    data = {
        'patient_id': session['id']
    }
    x = HeartRate.plotHeartRate(data)
    y = BloodPressure.plotbloodPressure(data)
    z = BloodSugar.plotbloodSugar(data)

    return render_template("patient/dashboard/vitals.html", first_name=session['first_name'])


@app.route('/vitalsPage/add')
def vitalsAdd():
    if session['loggedIn'] == False:
        return render_template('/')
    return render_template("patient/dashboard/forms/vitalsAdd.html", first_name=session['first_name'])


# ************************ Account ********************************** #


@app.route('/accountPage')
def accountPage():
    if session['loggedIn'] == False:
        return render_template('/')
    data = {
        "email": session['email']
    }

    userInfo = Patient.getUserByEmail(data)
    return render_template("patient/dashboard/account.html", first_name=session['first_name'], user=userInfo)


@app.route('/accountPage/edit')
def editAccountPage():
    if session['loggedIn'] == False:
        return render_template('/')
    data = {
        "email": session['email']
    }
    userInfo = Patient.getUserByEmail(data)

    return render_template("patient/dashboard/forms/accountEdit.html", first_name=session['first_name'], user=userInfo)
