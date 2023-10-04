import math
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
# rcParams['font.family'] = 'Montserrat'
# rcParams['Montserrat'] = ["sans-serif"]
import matplotlib

matplotlib.use('agg')

class HeartRate:
    def __init__(self, data):
        self.id = data['id']
        self.heart_rate = data['heart_rate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.patient_id = data['patient_id']
    
    @staticmethod
    def insertHeartRate(data):
        query = "INSERT INTO heart_rate_data (heart_rate, patient_id) VALUES(%(heart_rate)s, %(patient_id)s) "
        newID = connectToMySQL("health_check").query_db(query, data)
        return newID
    
    @staticmethod
    def plotHeartRate(data):
        query = "SELECT id,heart_rate from heart_rate_data WHERE patient_id = %(patient_id)s"
        result = connectToMySQL("health_check").query_db(query, data)
        id = []
        heartRate = []
        for i in result:
            id.append(i['id'])
            heartRate.append(i['heart_rate'])
        plt.clf()
        plt.plot(id,heartRate, color = "#0096FF", marker = ".", markersize = 20)
        plt.title('Heart Rate')
        plt.xlabel('Data Point')
        plt.ylabel('Heart Rate (bpm)')
        plt.savefig("flask_app/static/imgs/heartRate.png", bbox_inches='tight')
        plt.show()
        return 0

    @classmethod
    def getLastHeartRate(cls, data):
        query = "SELECT * from heart_rate_data WHERE patient_id = %(patient_id)s ORDER BY id DESC limit 1"
        result = connectToMySQL("health_check").query_db(query, data)

        heartRate = []

        for data in result:
            heartRate.append(cls(data))
        
        if len(heartRate) == 0:
            print("No Data")
            heartRate = "No Data"
        else:
            heartRate = heartRate[0]
        
        return heartRate








class BloodPressure:
    def __init__(self, data):
        self.id = data['id']
        self.systolic_data = data['systolic_data']
        self.diastolic_data = data['diastolic_data']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.patient_id = data['patient_id']

    
    @staticmethod
    def insertBloodPressure(data):
        query = "INSERT INTO blood_pressure_data (systolic_data, diastolic_data, patient_id) VALUES(%(systolic_data)s, %(diastolic_data)s, %(patient_id)s) "
        newID = connectToMySQL("health_check").query_db(query, data)
        return newID

    @staticmethod
    def plotbloodPressure(data):
        query = "SELECT id, systolic_data, diastolic_data from blood_pressure_data WHERE patient_id = %(patient_id)s"
        result = connectToMySQL("health_check").query_db(query, data)
        id = []
        systolic_data = []
        diastolic_data = []
        for i in result:
            id.append(i['id'])
            systolic_data.append(i['systolic_data'])
            diastolic_data.append(i['diastolic_data'])
        plt.clf()
        plt.plot(id,systolic_data, color = "#5800FF", label = "Systolic", marker = ".", markersize = 20)
        plt.plot(id,diastolic_data, color = "#00D7FF", label = "Diastolic", marker = ".", markersize = 20)
        plt.legend()
        plt.title("Blood Pressure")
        plt.xlabel("Data Point")
        plt.ylabel("Blood Pressure (mmHg)")
        plt.savefig("flask_app/static/imgs/bloodPressure.png", bbox_inches='tight')
        plt.show()
        return 0

    @classmethod
    def getLastBP(cls, data):
        query = "SELECT * from blood_pressure_data WHERE patient_id = %(patient_id)s ORDER BY id DESC limit 1"
        result = connectToMySQL("health_check").query_db(query, data)

        bloodPressure = []

        for data in result:
            bloodPressure.append(cls(data))

        if len(bloodPressure) == 0:
            print("No Data")
            bloodPressure = "No Data"
        else:
            bloodPressure = bloodPressure[0]
        return bloodPressure               









class BloodSugar:
    def __init__(self, data):
        self.id = data['id']
        self.blood_sugar_mg_dl = data['blood_sugar_mg_dl']
        self.blood_sugar_mmol_l = data['blood_sugar_mmol_l']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.patient_id = data['patient_id']

    @staticmethod
    def insertBloodSugar(data):
        query = "INSERT INTO blood_sugar_data (blood_sugar_mg_dl, blood_sugar_mmol_l, patient_id) VALUES(%(blood_sugar_mg_dl)s, %(blood_sugar_mmol_l)s, %(patient_id)s) "
        newID = connectToMySQL("health_check").query_db(query, data)
        print(newID)
        return newID

    @staticmethod
    def plotbloodSugar(data):
        query = "SELECT id, blood_sugar_mmol_l, blood_sugar_mg_dl from blood_sugar_data WHERE patient_id = %(patient_id)s"
        result = connectToMySQL("health_check").query_db(query, data)
        id = []
        blood_sugar_mmol_l = []
        blood_sugar_mg_dl = []
        for i in result:
            id.append(i['id'])
            blood_sugar_mmol_l.append(i['blood_sugar_mmol_l'])
            blood_sugar_mg_dl.append(i['blood_sugar_mg_dl'])
        plt.clf()
        plt.plot(id,blood_sugar_mmol_l, color = "#5800FF", label = "mM", marker = ".", markersize = 20)
        plt.title("Blood Sugar")
        plt.xlabel("Data Point")
        plt.ylabel("Blood Sugar (mH)")
        plt.savefig("flask_app/static/imgs/bloodSugar.png", bbox_inches='tight')
        plt.show()
        return 0

    

    @classmethod
    def getLastBloodSugar(cls, data):
        query = "SELECT * from blood_sugar_data WHERE patient_id = %(patient_id)s ORDER BY id DESC limit 1"
        result = connectToMySQL("health_check").query_db(query, data)

        bloodSugar = []

        for data in result:
            bloodSugar.append(cls(data))
        
        if len(result) == 0:
            bloodSugar = "No Data"
        else:
            bloodSugar = bloodSugar[0]
        return bloodSugar




    
