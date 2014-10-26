"""
This function takes in the generated list of student objects and the
dict of course objects. Students that are able to be placed into a
preferred course are added to the student list associated with each
course, and a list of unsorted students is returned.
"""
def sortStudents(students, courses):
    # Ensure students are sorted, based on time submitted or, if those
    # are equal, by student id. Uses property of Python tuple sorting.
    students.sort(key=lambda student: (student.getTimeSubmitted(), student.getStudentId()))

    #for student in students:
    #    print("Time: {}".format(student.getTimeSubmitted()))

    unsorted_students = []

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
                    pass
            except KeyError:
                print "Error with course {}".format(preference)
                # Course was not in list of courses.
                continue
        if not placed:
            unsorted_students.append(student)

    return unsorted_students
