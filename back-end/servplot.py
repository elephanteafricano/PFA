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


def plot_smoking_history_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='smoking_history', hue='diabetes', data=df)
    plt.title('Relation entre le tabagisme et le diabète')
    plt.xlabel('Historique de tabagisme')
    plt.ylabel('Nombre de personnes')
    plt.legend(title='Diabète', loc='upper right')



def plot_bmi_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='diabetes', y='bmi', data=df)
    plt.title('Relation entre l\'IMC et le diabète')
    plt.xlabel('Diabète')
    plt.ylabel('IMC')
  

def plot_HbA1c_level_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='diabetes', y='HbA1c_level', data=df)
    plt.title('Relation entre le niveau de HbA1c et le diabète')
    plt.xlabel('Diabète')
    plt.ylabel('Niveau de HbA1c')
 

def plot_blood_glucose_level_vs_diabetes(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='diabetes', y='blood_glucose_level', data=df)
    plt.title('Relation entre le niveau de glucose sanguin et le diabète')
    plt.xlabel('Diabète')
    plt.ylabel('Niveau de glucose sanguin')
 





def generate_bmi_plot(bmi):
    # Définir les catégories de l'IMC et leurs représentations de couleur
    categories = ['Insuffisance pondérale', 'Poids normal', 'Surpoids', 'Obésité classe I', 'Obésité classe II']
    colors = ['#ADD8E6', '#90EE90', '#FFFFE0', '#FFD700', '#FFB6C1']
    boundaries = [16.0, 18.5, 25.0, 30.0, 35.0, 40.0]  # Ajout d'une limite supérieure

    # Créer une nouvelle figure et un axe
    fig, ax = plt.subplots(figsize=(14, 4))  # Augmenter la taille de la figure
    
    # Parcourir les catégories et dessiner des barres horizontales pour chaque catégorie
    for idx, category in enumerate(categories):
        # Dessiner une barre horizontale pour chaque catégorie
        if idx < len(boundaries) - 1:
            ax.barh(0, boundaries[idx + 1] - boundaries[idx], left=boundaries[idx], color=colors[idx], edgecolor='black')

    # Dessiner une ligne verticale pour l'IMC de l'utilisateur
    ax.axvline(bmi, color='black', linewidth=2)
    ax.text(bmi + 0.1, 0, f'Votre IMC: {bmi:.2f}', va='center', ha='left', fontsize=12, fontweight='bold')

    # Supprimer les marqueurs et les étiquettes de l'axe y
    ax.set_yticks([])
    # Définir les limites de l'axe x
    ax.set_xlim(16, 40)
    # Définir les positions des étiquettes de l'axe x et les étiqueter avec les catégories de l'IMC
    ax.set_xticks(boundaries[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold', rotation=45, ha='right')  # Rotation des étiquettes
    
    # Titre du graphe
    plt.title('Catégories de l\'IMC', fontsize=14, fontweight='bold')
    # Étiquette de l'axe x
    plt.xlabel('IMC', fontsize=12, fontweight='bold')
    
    # Ajuster la disposition du graphe
    plt.tight_layout()
    # Afficher une grille en pointillés pour une meilleure lisibilité
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Sauvegarder le graphe sous forme d'image
    plt.savefig('static/bmi_plot.png', bbox_inches='tight')
    # Fermer la figure pour libérer la mémoire
    plt.close()

def generate_hba1c_plot(hba1c):
    # Définir les catégories d'HbA1c et leurs représentations de couleur
    categories = ['Optimal', 'Elevée', 'Haut']
    colors = ['#90EE90', '#FFD700', '#FF4500']
    boundaries = [0, 5.7, 6.4, 10.0]

    # Créer une nouvelle figure et un axe
    fig, ax = plt.subplots(figsize=(14, 4))  # Augmenter la taille de la figure
    
    # Parcourir les catégories et dessiner des barres horizontales pour chaque catégorie
    for idx, category in enumerate(categories):
        # Dessiner une barre horizontale pour chaque catégorie
        if idx < len(boundaries) - 1:
            ax.barh(0, boundaries[idx + 1] - boundaries[idx], left=boundaries[idx], color=colors[idx], edgecolor='black')

    # Dessiner une ligne verticale pour le niveau d'HbA1c de l'utilisateur
    ax.axvline(hba1c, color='black', linewidth=2, linestyle='--')
    ax.text(hba1c + 0.1, 0, f'Votre HbA1c: {hba1c:.2f}%', va='center', ha='left', fontsize=12, fontweight='bold')

    # Supprimer les marqueurs et les étiquettes de l'axe y
    ax.set_yticks([])
    # Définir les limites de l'axe x
    ax.set_xlim(0, 10)
    # Définir les positions des étiquettes de l'axe x et les étiqueter avec les catégories d'HbA1c
    ax.set_xticks(boundaries[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold', rotation=0, ha='center')  # Rotation des étiquettes
    
    # Titre du graphe
    plt.title('Catégories de HbA1c', fontsize=14, fontweight='bold')
    # Étiquette de l'axe x
    plt.xlabel('HbA1c (%)', fontsize=12, fontweight='bold')
    
    # Ajuster la disposition du graphe
    plt.tight_layout()
    # Afficher une grille en pointillés pour une meilleure lisibilité
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Sauvegarder le graphe sous forme d'image
    plt.savefig('static/hba1c_plot.png', bbox_inches='tight')
    # Fermer la figure pour libérer la mémoire
    plt.close()

 

def generate_blood_glucose_level_plot(glucose_level):
    # Définir les catégories de glucose sanguin et leurs représentations de couleur
    categories = ['Faible','Normale', 'Elevée', 'Haut']
    colors = ['#FFFFE0','#90EE90', '#FFD700', '#FF4500']
    boundaries = [0,70, 100, 125, 200]

    # Créer une nouvelle figure et un axe
    fig, ax = plt.subplots(figsize=(14, 4))  # Augmenter la taille de la figure
    
    # Parcourir les catégories et dessiner des barres horizontales pour chaque catégorie
    for idx, category in enumerate(categories):
        # Dessiner une barre horizontale pour chaque catégorie
        if idx < len(boundaries) - 1:
            ax.barh(0, boundaries[idx + 1] - boundaries[idx], left=boundaries[idx], color=colors[idx], edgecolor='black')

    # Dessiner une ligne verticale pour le niveau de glucose sanguin de l'utilisateur
    ax.axvline(glucose_level, color='black', linewidth=2, linestyle='--')
    ax.text(glucose_level + 1, 0, f'Votre glucose: {glucose_level:.1f} mg/dL', va='center', ha='left', fontsize=12, fontweight='bold')

    # Supprimer les marqueurs et les étiquettes de l'axe y
    ax.set_yticks([])
    # Définir les limites de l'axe x
    ax.set_xlim(0, 200)
    # Définir les positions des étiquettes de l'axe x et les étiqueter avec les catégories de glucose sanguin
    ax.set_xticks(boundaries[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold', rotation=0, ha='center')  # Rotation des étiquettes
    
    # Titre du graphe
    plt.title('Catégories de glucose sanguin', fontsize=14, fontweight='bold')
    # Étiquette de l'axe x
    plt.xlabel('Glucose sanguin (mg/dL)', fontsize=12, fontweight='bold')
    
    # Ajuster la disposition du graphe
    plt.tight_layout()
    # Afficher une grille en pointillés pour une meilleure lisibilité
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Sauvegarder le graphe sous forme d'image
    plt.savefig('static/blood_glucose_level_plot.png', bbox_inches='tight')
    # Fermer la figure pour libérer la mémoire
    plt.close()