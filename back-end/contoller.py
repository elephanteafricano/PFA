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