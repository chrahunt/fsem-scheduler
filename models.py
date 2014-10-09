# Here is where we'd put our classes, if we had any!

class Course(object):
    def __init__(self, course_name, seats):
        self.course_name = course_name
        self.seats = seats
    	self.students = []

    def addStudent(Student):
	self.students.append(Student)
    
    def removeStudent(Student):
	self.students.remove(Student)

    def getStudents():
	return self.students

    def setSeats(numSeats):
	self.seats = numSeats

    def isFull():
	if len(self.students) == len(self.students):
		return true
	else:
		return false

class Student(object):
    def __init__(self, name, email, time_submitted, pref_one=None, pref_two=None, pref_three=None):
        self.name = name
	#dont worry about email till we have confirmation from mellinger
	self.email = email
        self.preferences = []
        self.raw_preferences = []
        # loop through and process the preferences, putting each into the raw preferences
        # and parsing to get the course name into the preferences.
	self.time_submitted = time_submitted
    
    def getPreferences():
	return self.preferences

    def getRawPreferences():
	return self.raw_preferences

    def getName():
	return self.name

    def getEmail()
	return self.email

    def getTimeSubmitted()
	return self.time_submitted
