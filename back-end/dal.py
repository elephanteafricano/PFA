import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import re
from typing import List
from dataclasses import dataclass
import pandas as pa
from sklearn.ensemble import RandomForestClassifier

from models import *

plt.style.use('ggplot')

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
        # Créer des listes de colonnes numériques et catégorielles
        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        categorical_features = X.select_dtypes(include=['object']).columns

        # Définir les transformateurs pour les variables numériques et catégorielles
        numeric_transformer = ImbPipeline(steps=[
            ('scaler', StandardScaler())
        ])

        categorical_transformer = ImbPipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Appliquer les transformations aux colonnes
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # Créer un pipeline avec SMOTE et RandomForestClassifier
        pipeline_rf = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', RandomForestClassifier(random_state=42))
        ])
Data_atv.correlation(df)
df=Data_atv.itrft(df)
# Séparer les fonctionnalités et la cible
X = df.drop('diabetes', axis=1)
y = df['diabetes']


#Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)