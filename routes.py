from server import *
from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from flask_table import Table, Col, OptCol
from datetime import datetime

@app.route("/",methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    return render_template("base.html", title="Internet Help Page");


@app.route("/providerpage",methods=["POST","GET"])
@login_required
def providerpage():
    providerId = request.args.get('providerId')
    rating=None
    for provider in system.getUserList():
        if provider.getEmail() == providerId and provider.getType() == "Provider":
            name = provider.getName()
            rating = averageRating(name)
            print("rating is " + str(rating))
            provider._rating = rating
            if request.method == "POST":
                rating = request.form["rating"]
                addRating(name, rating)
                return render_template("provider_profile.html",title="Provider Profile",provider=provider,rating=rating,rate=False)
            else:
                return render_template("provider_profile.html",title="Provider Profile",provider=provider,rating=rating, rate=request.args.get('rate'))
    return 'OK'


@app.route("/centrepage",methods=["POST","GET"])
@login_required
def centrepage():
    centreId = request.args.get('centreId')
    centreRating = averageRating(centreId)
    #print("centre rating is " + str(centre._rating) + " for " + centreId)
    for centre in system.getCentreList():
        if centre.getName() == centreId:
            centre._rating = centreRating
            providers=[]
            for user in system.getUserList():
                if user.getType() == "Provider":
                    workplaces = []
                    for workplace in user.getWorkplaces():
                        workplaces.append(workplace.getName())
                    if centre.getName() in workplaces:
                        user._rating = averageRating(user.getName())
                        #print("rating is " + str(user._rating) + " for " + user._name)
                        providers.append(user)
            if request.method == "POST":
                rating = request.form["rating"]
                addRating(centreId, rating)
                return render_template("centre_profile.html",title="Centre Profile",centre=centre,providers=providers,centreRating=centreRating,rate=False)
            else:
                return render_template("centre_profile.html",title="Centre Profile",centre=centre,providers=providers,centreRating=centreRating,rate=request.args.get('rate'))
    return '404'

@app.route("/appointments", methods=["POST", "GET"])
@login_required
def appointments():
    AppointmentsList = loadAppointments(current_user)
    table = AppointmentTable(AppointmentsList, no_items=None)
    return render_template("viewAppointments.html", title="Appointments", show=True, table=table)

@app.route("/patientList", methods=["POST", "GET"])
@login_required
def patientList():
    PatientList = loadPatients(current_user)
    print(current_user.getType())
    table = PatientTable(PatientList)
    return render_template("PatientList.html", title="All Patients", show=True, table=table)

@app.route("/patientHistory", methods=["POST", "GET"])
@login_required
def patientHistory():

    if request.method == "POST":
        appointmentId = request.form["appointmentId"]
        newNote = request.form["editNote"]
        print("new note is: " + newNote + " for " + appointmentId)
        #write to csv

    userName = request.args.get('userName')
    HistoryList = loadHistory(current_user, userName)
    #print("dict issss", HistoryList)
    return render_template("PatientHistory.html", title="All Patients", show=True, historyList=HistoryList, note="N/A", userName=userName)



    #historyTable = HistoryTable(HistoryList)
    #historyTable.add_column('Edit', ButtonCol('Edit', 'patientHistory',button_attrs={'class': 'btn btn-info', 'data-toggle': "modal", 'data-target': "#myModal", 'type': 'button'}, form_attrs={'type': "disabled"} ))
    #historyTable.add_column('_note', Col("Doctors Notes"))
    #td_html_attrs={'class': 'btn btn-link'}
    #flask.request.endpoint, **dict(flask.request.view_args, **args)
