from classes import *
import csv
import operator

#Usage: pass in "LoadAll" to find all appointments with all attributes
#Pass in a user's name or email to find all their appointments without all attributes
def loadAppointments(user):
    UserAppointmentList = []
    with open('appointments.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        if user == "LoadAll":
            for row in  csv_reader:
                email = row[0]; providerName = row[3];
                lastName = row[2]; centreName = row[4]; date = row[5];
                time = row[6]; reason = row[7]; note = row[8];
                identifier = row[9]; firstName = row[1];
                appointment = Appointment(firstName, lastName, providerName, centreName, date, time, reason, note, identifier)
                UserAppointmentList.append(appointment)
        else:
            for row in csv_reader:
                email = row[0]
                providerName = row[3]
                if(providerName == user.getName() or user.getEmail() == (email)):
                    firstName = row[1]
                    lastName = row[2]
                    centreName = row[4]
                    date = row[5]
                    time = row[6]
                    reason = row[7]
                    identifier = row[9]
                    appointment = Appointment(firstName, lastName, providerName, centreName, date, time, reason)
                    UserAppointmentList.append(appointment)
    #UserAppointmentList = sorted(UserAppointmentList, key = lambda x: (Appointment.date))
    UserAppointmentList = sorted(UserAppointmentList, key=(operator.attrgetter('_date','_timeIndex')))
    return UserAppointmentList

def loadCentres():
	CentreList = []
	with open('health_centres.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			type = row[0][1:-1]
			code = row[1][2:-1]
			name = row[2][2:-1]
			contact = row[3][2:-1]
			suburb = row[4][2:-1]
			CentreList.append(Centre(name,code,type,contact,suburb))
	return CentreList

def loadProviders():
	#def __init__(self,name='',email='',password='',field='',appointments=[]):
	ProviderList = []
	with open('provider.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			name = row[0][0:row[0].find("@")].capitalize()
			email = row[0]#[1:-1]
			password = row[1]#[2:-1]
			field = row[2]#[2:-1]

			workplaces = []
			with open('provider_health_centre.csv') as prov_file:
				prov_reader = csv.reader(prov_file, delimiter=',')
				for entry in prov_reader:
					if entry[0] == email:
						for centre in loadCentres():
							if centre.getName() == entry[1]:
								workplaces.append(centre)

			ProviderList.append(Provider(name,email,password,[],workplaces,field))
	'''
	for prov in ProviderList:
		print(prov.getName() + " works at:")
		print(prov.getWorkplaces())
	'''
	return ProviderList

def loadPatients():
	PatientList = []
	with open('patient.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			name = row[0][0:row[0].find("@")].capitalize()
			email = row[0]#[1:-1]
			password = row[1]#[2:-1]
			PatientList.append(Patient(name,email,password,[]))
	return PatientList

def loadUsers():
	UserList = []
	UserList += loadPatients()
	UserList += loadProviders()
	return UserList

def loadRatings(name):
    with open('ratings.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        ratings = []
        for row in csv_reader:
            ID = row[0]
            if ID == name:
                ratings.append(row[1])
    return ratings

def addRating(name, rating):
    with open('ratings.csv','a') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(csv_file, lineterminator='\n')
        line = [name, rating]
        csv_writer.writerow(line)
