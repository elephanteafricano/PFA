import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from typing import List
from dataclasses import dataclass
import pandas as pa
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

df = DataEtl.extract("/Users/macbookpro/PFA/diabetes_prediction_dataset.csv")

df = pd.DataFrame(df)

@dataclass
class Data_atv:
    def correlation(data):
        num_cols = ['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']
        df = pd.DataFrame(data, columns=num_cols)  
        plt.figure(figsize=(8, 5))
        sns.heatmap(df.corr(), cmap='coolwarm', annot=True, cbar=False)
        plt.show()
        
Data_atv.correlation(df)
