from server import *
from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from flask_table import Table, Col, OptCol
from datetime import datetime

@app.route("/",methods=["GET"])
#@app.route("/home", methods=["GET"])
def index():
    message1 = ['a', 'b']
    message1[0] = "To go to a page: "
    message1[1] = "click the corresponding button in the table below."
    message2 = ['a', 'b']
    message2[0] = "To zoom in: "
    message2[1] = "press the CTRL key and + key at the same time. Use CTRL and - to zoom out."
    message3 = ['a', 'b']
    message3[0] = "To scroll: "
    message3[1] = "(move the page up or down) by using the wheel in the center of the mouse, or by moving the vertical bar on the right up and down."
    messages = [message1,message2,message3]
    return render_template("homepage.html", title="Internet Help Page", messages=messages);

@app.route("/news",methods=["GET"])
def news():
    return render_template("news.html", title="News");

@app.route("/trip",methods=["GET"])
def trip():
    return render_template("tripPlanner.html", title="Trip Planner");

@app.route("/weather",methods=["GET"])
def weather():
    return render_template("weather.html", title="Trip Planner");
