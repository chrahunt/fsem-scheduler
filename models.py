import re

# The Course class represents a FSEM into which a student may be placed.
# The Course class is responsible for holding the information related to
# the course it represents, as well as managing the list of students
# that have been assigned to the course.
class Course(object):
    def __init__(self, course_name, seats):
        self.course_name = course_name
        self.seats = int(seats)
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
        self.seats += int(numSeats)

    def getSeats(self):
        return self.seats

    def isFull(self):
        return len(self.students) == self.seats


class Student(object):
    # The Student class requires, at a minimum, the first name, last
    #   name, time submitted, and student id. The names of the
    #   parameters for this constructor should match the values of
    #   student_headers in parse.py, so that iteration over those values
    #   can construct a dictionary to be passed in to __init__ here.
    def __init__(self, first_name, last_name, time_submitted, student_id, pref_one=None, pref_two=None, pref_three=None):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
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
            result = re.split("(.*?) - .*", pref)
            if not(len(result) == 1):
                self.preferences.append(result[1])

    # Return the array of strings containing only the course numbers of
    # the preferred classes for an individual.
    def getPreferences(self):
        return self.preferences

    # Returns an array of preferences as they appeared in the spreadsheet
    def getRawPreferences(self):
        return self.raw_preferences

    # Returns the student's first name.
    def getFName(self):
        return self.first_name

    # Returns the student's last name.
    def getLName(self):
        return self.last_name

    # Returns the datetime object corresponding to the time and date
    # the student completed the survey.
    def getTimeSubmitted(self):
        return self.time_submitted

    def getStudentId(self):
        return self.student_id
