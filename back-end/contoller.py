from typing import Union
from models import User,Diabete
from flask import Flask, request, render_template, session, redirect, url_for, send_file
from typing import Union
import smtplib
import matplotlib
import numpy
from matplotlib import pyplot as plt 
from dal import *
from service import *
from servplot import *
import os

from fpdf import FPDF
matplotlib.use('agg') 

app = Flask(__name__)
app.secret_key = "$T@2023"

def verify_credentials(email, password) -> Union[User, None]:
    connection = DataBase.get_connection()
    cursor = connection.cursor()
    user_data =UserService.signin(email,password)
    if user_data !=None:
        user = User(email=user_data[0], password=user_data[1])
        return user
    else:
        return None

def save_plot(plot_func, filename):
    plt.figure()
    plot_func()
    plt.savefig(os.path.join('static', filename))
    plt.close()




@app.route("/")
def hello():
    return render_template('acceuil.html')


@app.route("/auth", methods=["GET","POST"])
def auth():
    email = request.form.get('email')
    pwd = request.form.get('password')
    connection = DataBase.get_connection()
    cursor = connection.cursor()
    user_data =UserService.signin(email,pwd)

    
    if user_data != None:
        session['email'] = email
        return redirect(url_for('plots'))
    else:
        return render_template('auth.html', error='Login or password error')
    

@app.route("/espaceMembre", methods=["GET","POST"])
def espaceMembre():
    return render_template('espaceMembre.html',)

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if 'email' not in session:
        return redirect(url_for('auth'))

    if request.method == "POST":
        email = session['email']
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        
  
        token = UserDao.generate_jwt(email)
        
     
        if UserDao.update_password_for_current_user(token, old_password, new_password):
            session.pop('email', None)
            return redirect(url_for('auth'))
        else:
            return render_template('change_password.html', error="Invalid old password")
    
    return render_template('change_password.html')


@app.route("/TesterDiabet", methods=["GET", "POST"])
def Pagedetest():
    prediction = None
    conseils = None
    message = None

    if request.method == "POST":
        gender = request.form.get("gender")
        age = float(request.form.get("age"))
        
        hypertension = bool(int(request.form.get("hypertension")))
        heart_disease = bool(int(request.form.get("heart_disease")))
        
        smoking_history = request.form.get("smoking_history")
        weight = float(request.form.get("poids"))
        height = float(request.form.get("taille"))
        HbA1c_level = float(request.form.get("HbA1c_level"))
        blood_glucose_level = float(request.form.get("blood_glucose_level"))

        bmi = weight / (height ** 2)

        
        generate_bmi_plot(bmi)
        generate_hba1c_plot(HbA1c_level)

        generate_blood_glucose_level_plot(blood_glucose_level)

        pred = DiabeteService.tester(gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level)

        hypertension = int(hypertension)
        heart_disease = int(heart_disease)
        pred = int(pred)

        con = DataBase.get_connection()
        cursor = con.cursor()
        try:
            insert_query = "INSERT INTO nos_utilisateur (gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, diabetes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, pred)
            cursor.execute(insert_query, values)
            con.commit()
        except Exception as e:
            print(e)
        finally:
            con.close()

        prediction = ""
        conseils = "Voici quelques conseils pour améliorer votre santé :\n"
        message="Veuillez clickez sur le bouton pour accéder à vos conseils personnalisé, même si votre diagnostique est négatif."

        if pred == 0:
            prediction ="Votre résultat montre que vous êtes en bonne santé.\n"
            conseils += "Continuez à maintenir un mode de vie sain et équilibré.\n"

            if smoking_history.lower() in ["current", "former"]:
                conseils += " - Envisagez des programmes pour arrêter de fumer, comme des thérapies de remplacement de la nicotine ou des médicaments prescrits.\n"
                conseils += " - Évitez les environnements où vous êtes exposé à la fumée secondaire. Demandez à votre entourage de ne pas fumer près de vous.\n"
                conseils += " - Rejoignez des groupes de soutien pour les fumeurs souhaitant arrêter, cela peut augmenter vos chances de succès.\n"
                conseils += " - Maintenez une routine d'exercices réguliers pour réduire les envies de fumer et améliorer votre santé pulmonaire.\n"
            
            if hypertension:
                conseils += " - Surveillez régulièrement votre tension artérielle. Utilisez un tensiomètre à domicile et notez vos résultats.\n"
                conseils += " - Réduisez votre consommation de sel à moins de 2 300 mg par jour. Préférez les herbes et les épices pour assaisonner vos plats.\n"
                conseils += " - Faites des exercices réguliers, comme la marche rapide, au moins 30 minutes par jour, cinq jours par semaine.\n"
                if age > 45:
                    conseils += " - Considérez des examens de tension artérielle plus fréquents, car le risque d'hypertension augmente avec l'âge.\n"

            if heart_disease:
                conseils += " - Consultez un cardiologue pour un suivi régulier et discutez des tests supplémentaires pour surveiller votre coeur.\n"
                conseils += " - Adoptez une alimentation riche en fruits, légumes, grains entiers, et poissons gras comme le saumon et le maquereau.\n"
                conseils += " - Limitez la consommation d'aliments riches en graisses saturées et trans, ainsi que les boissons sucrées.\n"
                conseils += " - Pratiquez des activités de relaxation comme le yoga ou la méditation pour réduire le stress.\n"
            
            if bmi > 25.0:
                conseils += " - Adoptez une alimentation équilibrée en intégrant plus de légumes, de fruits et de fibres. Limitez les aliments transformés et riches en calories.\n"
                conseils += " - Faites de l'exercice régulièrement. Essayez de faire au moins 150 minutes d'activité modérée ou 75 minutes d'activité vigoureuse par semaine.\n"
                conseils += " - Fixez-vous des objectifs de perte de poids réalistes, comme perdre 5 à 10 pourcent de votre poids corporel sur une période de six mois.\n"
                conseils += " - Surveillez votre poids régulièrement et tenez un journal alimentaire pour suivre vos habitudes alimentaires.\n"

            if HbA1c_level > 6.0:
                conseils += " - Contrôlez votre glycémie et suivez les recommandations de votre médecin pour ajuster votre alimentation et vos médicaments.\n"
                conseils += " - Suivez un régime à faible indice glycémique, comprenant des légumes, des grains entiers et des protéines maigres pour stabiliser votre glycémie.\n"
                conseils += " - Évitez les boissons sucrées et les aliments riches en sucre raffiné. Optez pour de l'eau, du thé sans sucre ou des boissons faibles en calories.\n"
                conseils += " - Faites des exercices physiques régulièrement, comme la marche, pour aider à contrôler votre glycémie.\n"

            if blood_glucose_level > 100.0:
                conseils += " - Mesurez régulièrement votre glycémie pour suivre vos progrès. Notez vos résultats et partagez-les avec votre médecin.\n"
                conseils += " - Limitez votre consommation de sucre et de glucides raffinés. Optez pour des alternatives plus saines comme les fruits frais et les grains entiers.\n"
                conseils += " - Mangez des repas équilibrés et évitez de sauter des repas. Des repas réguliers peuvent aider à stabiliser votre glycémie.\n"
                conseils += " - Intégrez des collations saines dans votre journée, comme des noix, des graines et des légumes crus.\n"
            if age > 60:
                conseils += " - Faites des bilans de santé réguliers pour surveiller les complications potentielles liées au diabète et à d'autres maladies chroniques.\n"
                conseils += " - Participez à des activités physiques adaptées à votre âge, comme le yoga, le tai-chi ou la natation.\n"

            if gender.lower() == "female" and age > 50:
                conseils += " - Surveillez votre densité osseuse et prenez des mesures pour prévenir l'ostéoporose, comme consommer suffisamment de calcium et de vitamine D.\n"
                conseils += " - Faites des exercices de renforcement musculaire pour maintenir votre masse musculaire et votre équilibre.\n"
            

        elif pred == 1:
            prediction = (
                "Votre résultat indique que vous êtes susceptible d'avoir le diabète de type 2.\n"
                "Les facteurs de risque identifiés dans votre profil incluent :\n"
            )
            if hypertension:
                prediction += " - Hypertension.\n"
                conseils += " - Surveillez régulièrement votre tension artérielle. Utilisez un tensiomètre à domicile et notez vos résultats.\n"
                conseils += " - Réduisez votre consommation de sel à moins de 2 300 mg par jour. Préférez les herbes et les épices pour assaisonner vos plats.\n"
                conseils += " - Faites des exercices réguliers, comme la marche rapide, au moins 30 minutes par jour, cinq jours par semaine.\n"
                if age > 45:
                    conseils += " - Considérez des examens de tension artérielle plus fréquents, car le risque d'hypertension augmente avec l'âge.\n"

            if heart_disease:
                prediction += " - Maladie cardiaque.\n"
                conseils += " - Consultez un cardiologue pour un suivi régulier et discutez des tests supplémentaires pour surveiller votre coeur.\n"
                conseils += " - Adoptez une alimentation riche en fruits, légumes, grains entiers, et poissons gras comme le saumon et le maquereau.\n"
                conseils += " - Limitez la consommation d'aliments riches en graisses saturées et trans, ainsi que les boissons sucrées.\n"
                conseils += " - Pratiquez des activités de relaxation comme le yoga ou la méditation pour réduire le stress.\n"

            if smoking_history.lower() in ["current", "former"]:
                prediction += " - Tabagisme.\n"
                conseils += " - Envisagez des programmes pour arrêter de fumer, comme des thérapies de remplacement de la nicotine ou des médicaments prescrits.\n"
                conseils += " - Évitez les environnements où vous êtes exposé à la fumée secondaire. Demandez à votre entourage de ne pas fumer près de vous.\n"
                conseils += " - Rejoignez des groupes de soutien pour les fumeurs souhaitant arrêter, cela peut augmenter vos chances de succès.\n"
                conseils += " - Maintenez une routine d'exercices réguliers pour réduire les envies de fumer et améliorer votre santé pulmonaire.\n"
            if bmi > 25.0:
                prediction += " - Surpoids.\n"
                conseils += " - Adoptez une alimentation équilibrée en intégrant plus de légumes, de fruits et de fibres. Limitez les aliments transformés et riches en calories.\n"
                conseils += " - Faites de l'exercice régulièrement. Essayez de faire au moins 150 minutes d'activité modérée ou 75 minutes d'activité vigoureuse par semaine.\n"
                conseils += " - Fixez-vous des objectifs de perte de poids réalistes, comme perdre 5 à 10 pourcent de votre poids corporel sur une période de six mois.\n"
                conseils += " - Surveillez votre poids régulièrement et tenez un journal alimentaire pour suivre vos habitudes alimentaires.\n"

            if HbA1c_level > 6.0:
                prediction += " - Niveau de HbA1c élevé.\n"
                conseils += " - Contrôlez votre glycémie et suivez les recommandations de votre médecin pour ajuster votre alimentation et vos médicaments.\n"
                conseils += " - Suivez un régime à faible indice glycémique, comprenant des légumes, des grains entiers et des protéines maigres pour stabiliser votre glycémie.\n"
                conseils += " - Évitez les boissons sucrées et les aliments riches en sucre raffiné. Optez pour de l'eau, du thé sans sucre ou des boissons faibles en calories.\n"
                conseils += " - Faites des exercices physiques régulièrement, comme la marche, pour aider à contrôler votre glycémie.\n"

            if blood_glucose_level > 100.0:
                prediction += " - Glycémie élevée.\n"
                conseils += " - Mesurez régulièrement votre glycémie pour suivre vos progrès. Notez vos résultats et partagez-les avec votre médecin.\n"
                conseils += " - Limitez votre consommation de sucre et de glucides raffinés. Optez pour des alternatives plus saines comme les fruits frais et les grains entiers.\n"
                conseils += " - Mangez des repas équilibrés et évitez de sauter des repas. Des repas réguliers peuvent aider à stabiliser votre glycémie.\n"
                conseils += " - Intégrez des collations saines dans votre journée, comme des noix, des graines et des légumes crus.\n"
            prediction += "Nous vous recommandons de consulter un médecin pour une confirmation et un traitement, mais avant tout, faites attention à ceci.\n"

        prediction_html = prediction.replace('\n', '<br>')
        conseils_html = conseils.replace('\n', '<br>')

        return render_template('testDiab.html', 
                               prediction=prediction_html, 
                               conseils=conseils_html,
                               gender=gender, 
                               age=age, 
                               hypertension=hypertension, 
                               heart_disease=heart_disease, 
                               smoking_history=smoking_history, 
                               poids=weight, 
                               taille=height, 
                               HbA1c_level=HbA1c_level, 
                               blood_glucose_level=blood_glucose_level,
                               message=message)
    return render_template('testDiab.html', prediction=prediction, conseils=conseils,message=message)






