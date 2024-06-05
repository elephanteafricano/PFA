create database db_diabete;
use db_diabete;

CREATE TABLE D_diabete (
    id INT PRIMARY KEY IDENTITY,
    gender varchar(10),
    age Float,
    hypertension BIT,
    heart_disease BIT,
    smoking_history varchar(20),
    bmi Float,
    blood_glucose_level Float,
    HbA1c_level Float,
    diabetes BIT
);
CREATE TABLE  usser (
    email varchar(50) PRIMARY KEY,
    password varchar(50)

);

CREATE TABLE nos_utilisateur(
    id INT PRIMARY KEY IDENTITY(1,1),
    gender VARCHAR(10),
    age FLOAT,
    hypertension BIT,
    heart_disease BIT,
    smoking_history VARCHAR(20),
    bmi FLOAT,
    blood_glucose_level FLOAT,
    HbA1c_level FLOAT,
    diabetes BIT
);
