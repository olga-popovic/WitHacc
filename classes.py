from abc import ABC
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol, ButtonCol

class Centre(object):
    def __init__(self,name='',code='',type='',contact='',suburb='',providers=[],rating=None):
        self._name = name
        self._code = code
        self._type = type
        self._contact = contact
        self._suburb = suburb
        self._providers = providers
        self._rating = rating

    def getName(self):
        return self._name

    def getCode(self):
        return self._code

    def getType(self):
        return self._type

    def getContact(self):
        return self._contact

    def getSuburb(self):
        return self._suburb

    def addProvider(self, provider):
        self._providers.append(provider)

    def getProviders(self):
        return self._providers

    def getRating(self):
        return self._rating

class User(UserMixin):
    def __init__(self,name='',email='',password='',appointments=[],type=""):
        self.id = email
        self._name = name
        self._email = email
        self._password = password
        self._appointments = appointments
        self._type = type

    def getName(self):
        return self._name

    def getEmail(self):
        return self._email

    def getPassword(self):
        return self._password

    def getAppointments(self):
        return self._appointments

    def getType(self):
        return self._type

    def addAppointment(self, appointment):
        self._appointments.append(appointment)

class Provider(User):
    def __init__(self,name='',email='',password='',appointments=[],workplaces=[],field="",rating=None):
        super().__init__(name,email,password,appointments,"Provider")
        self._workplaces = workplaces
        self._field = field
        self._rating = rating

    def getWorkplaces(self):
        return self._workplaces

    def addWorkplace(self, name):
        return self._workplaces.append(name)

    def getField(self):
        return self._field

    def getRating(self):
        return self._rating

class Patient(User):
    def __init__(self,name='',email='',password='',appointments=[]):
        super().__init__(name,email,password,appointments,"Patient")

class Appointment(object):
    def __init__(self,firstName='',lastName='',providerName='',centreName='',date='',time='',reason='',note='', identifier=''):
        self._firstName = firstName
        self._lastName = lastName
        self._providerName = providerName
        self._centreName = centreName
        self._date = date
        self._time = time
        self._timeIndex = int(time.replace(":",""))
        self._reason = reason
        self._note = note if note is not None else "N/A"
        self._identifier = identifier

    def getTimeIndex(self):
        return self._timeIndex

    def getDate(self):
        return self._date

class AppointmentTable(Table):
    '''def __init__(self,patientFirstName='',patientLastName='',providerName='',centreName='',date='',time='',reason=''):
        self._patientFirstName = patientFirstName
        self._patientLastName = patientLastName
        self._providerName = providerName
        self._centreName = centreName
        self._date = date
        self._time = time
        self._reason = reason'''

    _firstName = Col('Patient First Name:')
    _lastName = Col('Patient Last Name:')
    _providerName = Col('Doctor:')
    _centreName = Col('Centre:')
    _date = Col('Date:')
    _time = Col('Time:')
    _reason = Col('Reason for Appointment:')
    no_items = "No appointments Found"
    classes = ['table table-striped']


class PatientTable(Table):

#name = LinkCol('Name', 'single_item', url_kwargs=dict(id='id'), anchor_attrs={'class': 'myclass'})
    firstName = LinkCol('Name', 'patientHistory',url_kwargs=dict(userName='firstName'),attr='firstName')
    lastName = Col('Patient Last Name:')
    lastSeen = Col('Last Seen:')
    reason = Col('Reason for Appointment:')
    no_items = "No Appointments Found"
    classes = ['table table-striped']

class HistoryTable(Table):
    _firstName = Col('Patient First Name:')
    _lastName = Col('Patient Last Name:')
    _providerName = Col('Doctor:')
    _centreName = Col('Centre:')
    _date = Col('Date:')
    _time = Col('Time:')
    _reason = Col('Reason for Appointment:')
    _note = Col("Doctor's notes: ")
    #_edit = Col('Edit', td_html_attrs={'class': 'btn btn-primary', 'data-toggle': "modal", 'data-target': "#exampleModal"})
    no_items = "No appointments Found"
    classes = ['table table-striped']
    #, '''url_kwargs_extra=dict(popup=True)'''


