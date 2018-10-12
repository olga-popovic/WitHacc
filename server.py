#a function to read in from provider csv and return a list of class type Centres
import csv
import math
from classes import *
from system import *
from flask import Flask
from flask_login import LoginManager
from flask_table import Table, Col
import datetime
import operator
from decimal import *
from random import randint

app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

system = HAMS()

def writeAppointment(email='',firstName='',lastName='',providerName='',centreName='',date='',time='',reason='',note=''):
    with open('appointments.csv', mode='a') as file:
        file_writer = csv.writer(file, delimiter=',')
        if note is None or note == '':
            note = "N/A"
        identifier = generateUniqueAppointmentId()
        #find a new identifier not in the csv yet
        file_writer.writerow([email, firstName, lastName, providerName, centreName, date, time, reason, note, identifier])
#string metric
def MatchScore(text, textlist):
    bestScore = 0
    bestWord = ""
    for word in textlist:
        score = 0
        maxLen = len(word)
        if len(text) < maxLen:
            maxLen = len(text)
        for i in range(0,maxLen):
            for j in range(0,len(text) - i + 1):
                #print(i, j, text[j:j+i])
                if text[j:j+i].lower() in word.lower():
                    score += i*math.exp(i)
                #else:
                    #score -= i
        score = score/((abs(len(text) - len(word)))+len(text)/(len(word)+1))
        if score > bestScore:
            bestScore = score
            bestWord = word
        #print(text,"~~~~ =>",word,"=",score)
    if bestScore < 15:
        return None
    else:
        #print(text,"~~~~>",bestWord,"=",bestScore)
        return bestWord

def availableDate(user,time,date):
    UserAppointmentList = loadAppointments(user)
    print("about to be formatted: ",time.replace(":",""))
    formatTime = int(time.replace(":",""))
    print("Trying to book at",formatTime,date)
    for appointment in UserAppointmentList:
        print("Comparing with",appointment.getTimeIndex(),appointment.getDate())
        if formatTime == appointment.getTimeIndex():
            print("TIME MATCHES")
        if formatTime == appointment.getTimeIndex() and date == appointment.getDate():
            print("UHOH taken")
            return False
    print("Passed all")
    return True

def loadPatients(user):
    PatientList = []
    seen = 0
    with open('appointments.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            email = row[0]
            providerName = row[3]
            if( providerName == user.getName() or user.getEmail() == (email) ):
                for patient in PatientList:
                    if (patient['firstName'] == row[1]):
                        if (patient['lastSeen'] < row[5]):
                            patient[2] = row[5]
                        seen = 1
                        break
                if (seen == 1):
                    seen = 0
                    continue
                patient = {}
                patient['firstName'] = row[1]
                patient['lastName'] = row[2]
                patient['lastSeen'] = row[5]
                patient['reason'] = row[7]
                #print("dict is", patient)
                PatientList.append(patient)

    PatientList = sorted(PatientList, key=lambda patient: patient['lastSeen'])
    return PatientList

def loadHistory(user,patient):
    buttonID = 0
    UserHistoryList = []
    with open('appointments.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(row[1] == patient):
                email = row[0]
                providerName = row[3]
                firstName = row[1]
                lastName = row[2]
                centreName = row[4]
                date = row[5]
                time = row[6]
                reason = row[7]
                note = row[8]
                identifier = row[9]
                appointment = Appointment(firstName, lastName, providerName, centreName, date, time, reason, note, identifier)
                UserHistoryList.append(appointment)
    #UserAppointmentList = sorted(UserAppointmentList, key = lambda x: (Appointment.date))
    #(providerName == user.getName() or user.getEmail() == (email)) and
    UserHistoryList = sorted(UserHistoryList, key=(operator.attrgetter('_date','_timeIndex')))
    return UserHistoryList

def validTime(time):
    tempTime = str(time)
    if len(tempTime) != 5:
        return 0
    if tempTime[2] != ":":
        return 0
    tempTime = tempTime.replace(":","")
    try:
        tempTime = int(tempTime)
        return 1
    except:
        return 0

def averageRating(ID):
    ratings = list(map(int,loadRatings(ID)))
    if len(ratings) != 0:
        avg = sum(ratings)/Decimal(len(ratings))
        avg = round(avg, 2)
    else:
        avg = None
    return avg

def generateUniqueAppointmentId():
    newId = randint(10000,99999)
    usedIdList = []
    for appointment in system.getAppointmentList():
        usedIdList.append(appointment._identifier)
    if newId in usedIdList:
        newId = generateUniqueAppointmentId()
    return newId
