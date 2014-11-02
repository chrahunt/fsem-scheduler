"""
This function takes in the generated list of student objects and the
dict of course objects. Students that are able to be placed into a
preferred course are added to the student list associated with each
course, and returns a list and dict. The list contains unsorted
students and the dict contains classes that were in the students'
preferences but not found in the courses dict.
"""
def sortStudents(students, courses):
    # Ensure students are sorted, based on time submitted or, if those
    # are equal, by student id. Uses property of Python tuple sorting.
    students.sort(key=lambda student: (student.getTimeSubmitted(), student.getStudentId()))

    unsorted_students = []
    # Dict of missing courses with the preference name as the key and an array
    # of students that requested that course as the values.
    missing_courses = {}

    for student in students:
        placed = False
        preferences = student.getPreferences();
        #print preferences
        for preference in preferences:
            try:
                if not courses[preference].isFull():
                    courses[preference].addStudent(student)
                    placed = True
                    break
                else:
                    #print "Course {} is full!".format(courses[preference].getName())
                    # Keep track of request for full course here.
                    # Increment request counter on course.
                    courses[preference].incrementRequests()

            except KeyError:
                # Course not found in list of courses.
                # Keep track of courses that were requested but not in the course list.
                if not(preference in missing_courses):
                    missing_courses[preference] = []
                missing_courses[preference].append(student.getStudentId());
                continue
        if not placed:
            # Student was not assigned a class.
            unsorted_students.append(student)

    return unsorted_students, missing_courses
