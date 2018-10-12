from server import *
from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from flask_table import Table, Col, OptCol
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return get_user(id)

def get_user(id):
    return system.get_user(id)

@app.route("/", methods=['GET','POST'])
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        message = "Incorrect username or password"
        password = request.form["password"]
        if email == "":
            message = "Please enter an email"
            return render_template("login.html",title="Login",message=message)

        if password == "":
            message = "Please enter a password"
            return render_template("login.html",title="Login",message=message)

        users = system.getUserList()
        for user in users:
            if user.getEmail() == email and user.getPassword() == password:
                message = "Successful as " + user.getName() + " , a " + user.getType()
                login_user(user)
                return render_template("home.html",title="Home",message=message)
        return render_template("login.html",title="Login",message=message)
    else:
        return render_template("login.html",title="Login",message="")

@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    chosen = ""
    logout_user()
    return redirect(url_for("login"))

@app.route("/home", methods=["POST","GET"])
@login_required
def home():
    if current_user.is_authenticated:
        message = "Hello "
        #current_user.get_id()
        message = message + " " + current_user.getName()
    return render_template("home.html",title="Home",message=message)

@app.route("/book", methods=["POST","GET"])
@login_required
def book():
    chosenCentre = request.args.get('centre')
    chosenProvider = request.args.get('provider')
    print("centre: ",chosenCentre,"provider ",chosenProvider)
    errors = []
    warnings = []
    firstName = current_user.getName()
    if request.method == "POST":
        lastName = request.form["lastName"]

        providerName = chosenProvider
        centreName = chosenCentre

        print(providerName, centreName)

        date = request.form["date"]
        time = request.form["time"]

        reason = request.form["reason"]

        print("DATE: ",date)

        if firstName == "":
            errors.append("First Name")
        if lastName == "":
            errors.append("Last Name")
        if providerName == "":
            errors.append("Provider Name")
        if centreName == "":
            errors.append("Centre Name")
        if date == "":
            errors.append("Date")
        if time == "":
            errors.append("Time")

        centreList = loadCentres()
        centreNames = []
        for centre in centreList:
            centreNames.append(centre.getName())

        if centreName not in centreNames:
            warnings.append("'"+centreName + '" is not a centre listed under HAMS')

        providerList = loadProviders()
        providerNames = []
        for provider in providerList:
            providerNames.append(provider.getName())

        if providerName not in providerNames:
            warnings.append('"'+providerName + '" is not a provider listed under HAMS')

        dateFormat = "%Y-%m-%d"
        print("TIME:",time)
        if date != "" and time != "":
            flag = 0
            try:
                date  = datetime.strptime(request.form['date'], dateFormat)
            except:
                warnings.append("Please enter date as yyyy-mm-dd")
                flag = 1

            if validTime(time) == 0:
                warnings.append("Please enter time as HH:MM")
                flag = 1

            if flag != 1:
                if (availableDate(current_user,time,date) == False):
                    warnings.append("You already have an appointment at this time and date")

                for provider in providerList:
                    if provider.getName() == providerName:
                        print("Found correct provider")
                        if (availableDate(provider,time,date) == False):
                            warnings.append('"'+providerName + '" already has an appointment at this time')


        if errors != [] or warnings != []:
            return render_template("book.html",title="Book",errors=errors,warnings=warnings,booked=False,firstName=firstName,lastName="",centreName=chosenCentre,providerName=chosenProvider)

        appointment = Appointment(firstName,lastName,providerName,centreName,date,time,reason)
        current_user.addAppointment(appointment)

        writeAppointment(current_user.getEmail(),firstName,lastName,providerName,centreName,date,time,reason)
        return render_template("book.html",title="Book",errors=[],warnings=[],booked=True,firstName=firstName,lastName="",centreName=chosenCentre,providerName=chosenProvider)
    return render_template("book.html",title="Book",errors=[],warnings=[],booked=False,firstName=firstName,lastName="",centreName=chosenCentre,providerName=chosenProvider)
    #return render_template("book.html",title="Booked by centre",errors=[],warnings=[],booked=False,firstName=firstName,lastName="tempLast")

@app.route("/search", methods=["POST","GET"])
@login_required
def search():
    if request.method == "POST":
        term = request.form['term']
        type = request.form['type']
        show = True
        contentType = ""
        data = []
        matches = []
        if term != "":
            message = ""
            #message = "Search term: " + term + ". Searched by: " + type
            centres = system.getCentreList()
            users = system.getUserList()
            #first check if exact match is there
            if (type == "Centre name"):
                contentType = "Centre name"
                data = centres
                for centre in centres:
                    if ((centre.getName()).lower() == term.lower()):
                        matches.append(centre)

                if matches == []:
                    wordlist = []
                    for centre in centres:
                        wordlist.append(centre.getName())

                    tempTerm = MatchScore(term, wordlist)
                    if tempTerm != None:
                        for centre in centres:
                            if (centre.getName() == tempTerm):
                                matches.append(centre)
                        message = 'No results for "' + term + '" found. Searching instead for "' + tempTerm + '"'

                if matches == []:
                    message = 'No results for "' + term + '"'
                    show = False

            elif (type == "Suburb"):
                contentType = "Centre name"
                data = centres
                for centre in centres:
                    if ((centre.getSuburb()).lower() == term.lower()):
                        matches.append(centre)

                if matches == []:
                    wordlist = []
                    for centre in centres:
                        wordlist.append(centre.getSuburb())

                    tempTerm = MatchScore(term, wordlist)
                    if tempTerm != None:
                        for centre in centres:
                            if (centre.getSuburb() == tempTerm):
                                matches.append(centre)
                        message = 'No results for "' + term + '" found. Searching instead for "' + tempTerm + '"'

                if matches == []:
                    message = 'No results for "' + term + '"'
                    show = False

            elif (type == "Provider name"):
                contentType = "Provider name"
                data = users
                for user in users:
                    if ((user.getName()).lower() == term.lower() and
                        user.getType() == "Provider"):
                        matches.append(user)
                if matches == []:
                    wordlist = []
                    for user in users:
                        if (user.getType() == "Provider"):
                            wordlist.append(user.getName())
                    tempTerm = MatchScore(term, wordlist)
                    if tempTerm != None:
                        for user in users:
                            if (user.getName() == tempTerm):
                                matches.append(user)
                        message = 'No results for "' + term + '" found. Searching instead for "' + tempTerm + '"'

                if matches == []:
                    message = 'No results for "' + term + '"'
                    show = False

            elif (type == "Service"):
                contentType = "Provider name"
                data = users
                for user in users:
                    if ((user.getType() == "Provider")):
                        if ((user.getField()).lower() == term.lower()):
                            matches.append(user)

                if matches == []:
                    print("No service found")
                    wordlist = []
                    for user in users:
                        if ((user.getType() == "Provider")):
                            wordlist.append(user.getField())

                    tempTerm = MatchScore(term, wordlist)
                    if tempTerm != None:
                        for user in users:
                            if ((user.getType() == "Provider")):
                                if (user.getField() == tempTerm):
                                    matches.append(user)
                        message = message + 'No results for "' + term + '" found. Searching instead for "' + tempTerm + '"'
                if matches == []:
                    message = 'No results for "' + term + '"'
                    show = False

            else:
                matches = data
        else:
            message = "Enter a search term"
            show = False
        return render_template("search.html",title="Search",message=message,show=show,data=matches,contentType=contentType)
    else:
        return render_template("search.html",title="Search",message="")

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


