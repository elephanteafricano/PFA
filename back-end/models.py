from dataclasses import dataclass

@dataclass
class User:
    email:str
    password:str

    
@dataclass
class Diabete:
    gender:str
    age:float
    hypertension:bool
    heart_disease:bool
    smoking_history:str
    bmi:float
    HbA1c_level:float
    blood_glucose_level:float
    diabetes:bool
