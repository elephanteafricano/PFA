from dataclasses import dataclass
from dal import *

class UserService:
    def signin(email:str, password:str):
        user =UserDao.authenticate(email, password)
        
        if(user == None):
            print("error email or password invalide")
            return None
        else:
            print("Connected succffuly")
            return user
        
   
        
class DiabeteService:
    def tester(gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level):
        
        data=(gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level)

        return Machine_learning.preprocess_and_predict(data, dt)

    
    def search(id):
        list = DiabDao.getAll()
        for i in list:
            if(i[1]== id):
                return i
        return None

