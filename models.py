# Here is where we'd put our classes, if we had any!

class Course(object):
    def __init__(self, course_name, seats):
        self.course_name = course_name
        self.seats = seats

class Student(object):
    def __init__(self, name, email, pref_one=None, pref_two=None, pref_three=None):
        self.name = name
        self.email = email
        self.preferences = []
        self.raw_preferences = []
        # loop through and process the preferences, putting each into the raw preferences
        # and parsing to get the course name into the preferences.
