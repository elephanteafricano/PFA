from dal import *

def plot_gender_vs_diabetes(df):
    if df.empty:
        print("DataFrame is empty! Cannot plot gender vs diabetes.")
        return
    if 'gender' not in df.columns or 'diabetes' not in df.columns:
        print("Required columns for gender vs diabetes plot are missing!")
        return

    plt.figure(figsize=(10, 6))
    sns.countplot(x='gender', hue='diabetes', data=df)
    plt.title('Relation entre le genre et le diabète')
    plt.xlabel('Genre')
    plt.ylabel('Nombre de personnes')
    plt.legend(title='Diabète', loc='upper right')

def plot_age_vs_diabetes(df):
    if df.empty:
        print("DataFrame is empty! Cannot plot age vs diabetes.")
        return
    if 'age' not in df.columns or 'diabetes' not in df.columns:
        print("Required columns for age vs diabetes plot are missing!")
        return

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='diabetes', y='age', data=df)
    plt.title('Relation entre l\'âge et le diabète')
    plt.xlabel('Diabète')
    plt.ylabel('Âge')
    

def plot_hypertension_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='hypertension', hue='diabetes', data=df)
    plt.title('Relation entre l\'hypertension et le diabète')
    plt.xlabel('Hypertension')
    plt.ylabel('Nombre de personnes')
    plt.legend(title='Diabète', loc='upper right')

def plot_heart_disease_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='heart_disease', hue='diabetes', data=df)
    plt.title('Relation entre les maladies cardiaques et le diabète')
    plt.xlabel('Maladie cardiaque')
    plt.ylabel('Nombre de personnes')
    plt.legend(title='Diabète', loc='upper right')

def plot_bmi_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='diabetes', y='bmi', data=df)
    plt.title('Relation entre l\'IMC et le diabète')
    plt.xlabel('Diabète')
    plt.ylabel('IMC')