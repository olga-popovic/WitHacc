from server import *
from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from flask_table import Table, Col, OptCol
from datetime import datetime

@app.route("/",methods=["GET"])
#@app.route("/home", methods=["GET"])
def index():
    return render_template("homepage.html", title="Internet Help Page");

@app.route("/news",methods=["GET"])
def news():
    return render_template("news.html", title="News");

@app.route("/trip",methods=["GET"])
def trip():
    return render_template("tripPlanner.html", title="News");