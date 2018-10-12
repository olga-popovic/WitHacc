from data_generator import *

class HAMS(ABC):
	def __init__(self):
		self._centreList = loadCentres()
		self._userList = loadUsers()
		self._appointmentList = loadAppointments("LoadAll")

	def getUserList(self):
		return self._userList

	def addUser(newUser):
		return (self._userList).append(newUser)

	def getCentreList(self):
		return self._centreList

	def addCentre(newCentre):
		self._centreList.append(newCentre)

	def get_user(self, id):
		for user in self._userList:
			if user.getEmail() == id:
				return user

	def getAppointmentList(self):
		return self._appointmentList