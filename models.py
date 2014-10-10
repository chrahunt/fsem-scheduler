import re

# The Course class represents a FSEM into which a student may be placed.
# The Course class is responsible for holding the information related to
# the course it represents, as well as managing the list of students
# that have been assigned to the course.
class Course(object):
    def __init__(self, course_name, seats):
        self.course_name = course_name
        self.seats = seats
        self.students = []

    def getName(self):
        return self.course_name

    def addStudent(self, student):
        self.students.append(student)
    
    def removeStudent(self, student):
        self.students.remove(student)

    def getStudents(self):
        return self.students

    def addSeats(self, numSeats):
        self.seats += numSeats

    def getSeats(self):
        return self.seats

    def isFull(self):
        return len(self.students) == len(self.students)


class Student(object):
    def __init__(self, name, time_submitted, pref_one=None, pref_two=None, pref_three=None):
        self.name = name
        self.time_submitted = time_submitted

        self.preferences = []
        self.raw_preferences = []
        
        # Add spreadsheet inputs for preferences to raw_preferences array
        for pref in [pref_one, pref_two, pref_three]:
            if pref:
                self.raw_preferences.append(pref)

        # Parse preferences from spreadsheet and get the course number
        # (e.g. FSEM 100A)
        # TODO: Handle case where preference is not parsed correctly.
        for pref in self.raw_preferences:
            result = re.split("(.*?) - .*")
            if not(len(result) == 1):
                preferences.append(result[1])

    # Return the array of strings containing only the course numbers of
    # the preferred classes for an individual.
    def getPreferences(self):
        return self.preferences

    def getRawPreferences(self):
        return self.raw_preferences

    def getName(self):
        return self.name

    def getTimeSubmitted(self):
        return self.time_submitted
