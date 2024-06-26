import pyodbc as my
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn import tree
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

plt.style.use('ggplot')
import re
from typing import List
from dataclasses import dataclass
import pandas as pa
from models import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

@dataclass
class DataBase:
    def get_connection():
     return my.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ELEPHANTE\\MSSQLSERVER01;'  
            'DATABASE=db_diabete;'
            'Trusted_Connection=yes;'
        )

@dataclass
class DataEtl:
    #path:str
    def extract(path):
        df=pd.read_csv(path)
        df_clean=df[['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history','bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']]
        df_clean=df_clean.drop_duplicates()
        df_clean = df_clean.dropna()
        df = pd.DataFrame(df_clean)  
        #print(df_clean.isnull().sum())
        records = df_clean.to_records(index=False)
        return records
    
    def load(df_clean):
       con = DataBase.get_connection()
       cursor = con.cursor()
       try:        
        insert_query = "INSERT INTO d_diabete (gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, diabetes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"  
        values = [tuple(row) for row in df_clean.values] 
        cursor.executemany(insert_query, values)
        
        con.commit()
       except Exception as e:
           print(e)


df = DataEtl.extract("C:/Users/aze/Desktop/PPf/diabetes_prediction_dataset.csv")

df = pd.DataFrame(df)

@dataclass
class Data_atv:
    def correlation(data):
        num_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']
        df = pd.DataFrame(data, columns=num_cols)  
        plt.figure(figsize=(8, 5))
        sns.heatmap(df.corr(), cmap='coolwarm', annot=True, cbar=False)
        plt.show()
    def agedrps(data):


        df = pd.DataFrame(data)
        df['age_groups'] = pd.cut(df['age'], bins=[0, 12, 19, 29, 39, 54, 64, float('inf')],
                                    labels=['child', 'teenager', 'young adult', 'adult', 'midle aged', 'old',
                                            'senior']).astype('O')


        df['bmi_groups'] = pd.cut(df['bmi'], bins=[0, 18.4, 24.9, 29.9, float('inf')],
                                    labels=['under weight', 'normal', 'overweight', 'obese']).astype('O')
        
    def eda(data):
        df = pd.DataFrame(data)
        num_cols = [col for col in df.columns[:-1] if
                    (df[col].dtype != 'O') & (col not in ['hypertension', 'heart_disease'])]
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 8))
        ax = ax.flatten()
        boxplot_color = 'steelblue'
        for i, col in enumerate(num_cols):
            bp = ax[i].boxplot(df[col], vert=False)
            ax[i].set_title(col, fontsize=14, fontweight='bold')
            ax[i].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey')
            ax[i].set_yticklabels([])
        plt.tight_layout(pad=4.0)
        plt.show()

    def bmi(data):
        df = pd.DataFrame(data)
        plt.figure(figsize=(16, 5))
        plt.boxplot(df['bmi'], vert=False)
        plt.title("Distribution of BMI")
        plt.show()
    
    def d_count(data):
        df = pd.DataFrame(data)
        diabetes_counts = df['diabetes'].value_counts()

        plt.figure(figsize=(8, 8))
        plt.pie(diabetes_counts, labels=['Non-Diabetic', 'Diabetic'], autopct='%1.1f%%', startangle=140,
                colors=['#66c2a5', '#fc8d62'])
        plt.title('Diabetes Distribution', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.show()


    @staticmethod
    def itrft(df):

        df['HH'] = ((df['hypertension'] == 1) & (df['heart_disease'] == 1)).astype(int)
        df['AH'] = df['age'] * df['hypertension']
        df['AHD'] = df['age'] * df['heart_disease']
        df['BB'] = df['blood_glucose_level'] * df['bmi']

        df['gender'] = np.where(df['gender'].str.lower() == 'female', 0, 1)
        df['smoking_history'] = np.where((df['smoking_history'].str.lower() == 'never') | (df['smoking_history'].str.lower() == 'no info')| (df['smoking_history'].str.lower() == 'ever'), 0, 1)
        return df

@dataclass
class Machine_learning:

    def test_best_model():

        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        categorical_features = X.select_dtypes(include=['object']).columns


        numeric_transformer = ImbPipeline(steps=[
            ('scaler', StandardScaler())
        ])

        categorical_transformer = ImbPipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])


        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        
        pipeline_rf = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        pipeline_lr = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', LogisticRegression(class_weight='balanced'))
        ])

        pipeline_dt = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', DecisionTreeClassifier(max_depth=10, random_state=1, criterion='entropy'))
        ])
        
        pipeline_kn = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', KNeighborsClassifier(n_neighbors=5))
        ])

       
        pipeline_nn = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42))
        ])

        for name, pipeline in {'Random Forest': pipeline_rf, 'Logistic Regression': pipeline_lr,
                               'Decision Tree': pipeline_dt, 'K Nearest Neighbors': pipeline_kn,
                               'Neural Network': pipeline_nn}.items():
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
            print(name)
            print("Train Accuracy Score:", accuracy_score(y_train, pipeline.predict(X_train)))
            print("Test Accuracy Score:", accuracy_score(y_test, y_pred))
            print("Rapport de classification:\n", classification_report(y_test, y_pred))
            print("AUC:", roc_auc_score(y_test, y_pred_proba))
            print()
            
            
        plt.figure(figsize=(10, 8))
        for name, pipeline in {'Random Forest': pipeline_rf, 'Logistic Regression': pipeline_lr,
                               'Decision Tree': pipeline_dt, 'K Nearest Neighbors': pipeline_kn,
                               'Neural Network': pipeline_nn}.items():
            pred_prob = pipeline.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, pred_prob)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'{name} (AUC = {roc_auc:.2f})')

        plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
        plt.xlabel('Taux de faux positifs (FPR)')
        plt.ylabel('Taux de vrais positifs (TPR)')
        plt.title('Courbes ROC pour différents modèles')
        plt.legend(loc='lower right')
        plt.grid(True)
        plt.show()
    
    def train_decision_tree_model(X_train, y_train):
        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        categorical_features = X.select_dtypes(include=['object']).columns

        numeric_transformer = ImbPipeline(steps=[
            ('scaler', StandardScaler())
        ])

        categorical_transformer = ImbPipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        pipeline_dt = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', DecisionTreeClassifier(max_depth=10, random_state=1, criterion='entropy'))
        ])
        for name, pipeline in {'Decision Tree': pipeline_dt}.items():
         pipeline.fit(X_train, y_train)
        return pipeline

    def preprocess_and_predict(input_data, decision_tree_model):

        df = pd.DataFrame([input_data], columns=['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level'])
        df=Data_atv.itrft(df)
        prediction = decision_tree_model.predict(df)

        return prediction[0]
    
import jwt
import datetime

SECRET_KEY = "Elephanto_jwt"

class UserDao:

    @staticmethod
    def AddUser(email: str, password: str):
        query = "INSERT INTO usser (email, password) VALUES (?, ?)"
        values = (email, password)
        con = DataBase.get_connection()
        cursor = con.cursor()
        cursor.execute(query, values)
        con.commit()
        user = User(email=email, password=password)
        return user

    @staticmethod
    def authenticate(email: str, password: str):
        query = "SELECT * FROM usser WHERE email=? AND password=?"
        values = (email, password)
        con = DataBase.get_connection()
        cursor = con.cursor()
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            token = UserDao.generate_jwt(user[0])  
            return {"user": user, "token": token}
        else:
            return None

    @staticmethod
    def generate_jwt(email: str):
        payload = {
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_jwt(token: str):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    @staticmethod
    def update_password_for_current_user(token: str, old_password: str, new_password: str) -> bool:
        decoded_token = UserDao.verify_jwt(token)
        if not decoded_token:
            return False

        email = decoded_token['email']
        
        authenticate_query = "SELECT * FROM usser WHERE email = ? AND password = ?"
        authenticate_values = (email, old_password)
        con = DataBase.get_connection()
        cursor = con.cursor()
        cursor.execute(authenticate_query, authenticate_values)
        user = cursor.fetchone()

        if user:
            update_query = "UPDATE usser SET password = ? WHERE email = ?"
            update_values = (new_password, email)
            cursor.execute(update_query, update_values)
            con.commit()
            return True
        else:
            return False


@dataclass
class  DiabDao:
    def getAll():
        query = "Select gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, diabetes  from d_diabete"
        con = DataBase.get_connection()
        df = pd.read_sql(query, con)
        con.close()
        return df

df=DiabDao.getAll()
    
Data_atv.correlation(df)
Data_atv.eda(df)
Data_atv.bmi(df)
Data_atv.d_count(df)
df=Data_atv.itrft(df)


X = df.drop('diabetes', axis=1)
y = df['diabetes']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)