import math
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Appointment:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.description = data['description']
        self.frequency = data['frequency']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validateAddAppointment(data):
        is_valid = True
        if len(data['title']) < 2:
            is_valid = False
        
        return is_valid
    
    @classmethod 
    def insertAppointments(cls, data):
        query = "INSERT INTO appointment (title, start_time, end_time, description, frequency, users_id) VALUES (%(title)s, %(start_time)s, %(end_time)s, %(description)s, %(frequency)s, %(users_id)s)"
        result = connectToMySQL("health_check").query_db(query, data)
        return result

    @classmethod
    def getAppointments(cls, data):
        query = "SELECT * from appointment WHERE users_id = %(users_id)s ORDER BY start_time"
        result = connectToMySQL("health_check").query_db(query, data)
        appointments = []
        for appointment in result:
            appointments.append(cls(appointment))
        return appointments
    
    @staticmethod 
    def deleteAppointment(data):
        query = "DELETE from appointment WHERE id = %(id)s;"
        result = connectToMySQL("health_check").query_db(query, data)
        return result

    @classmethod
    def getOneAppointment(cls, data):
        query = "SELECT * from appointment WHERE users_id = %(users_id)s ORDER BY start_time limit 1"
        result = connectToMySQL("health_check").query_db(query, data)
        appointments = []
        for appointment in result:
            appointments.append(cls(appointment))

        if len(appointments) == 0 :
            appointments = "No appointment"
            print("No appointment")
        else:
            appointments = appointments[0]
        return appointments

