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