#a function to read in from provider csv and return a list of class type Centres
from flask import Flask
from flask_login import LoginManager
from flask_table import Table, Col

app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy
    