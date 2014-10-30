from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import xlrd, xlwt
import os
from datetime import datetime

from parse import get_student_headers, get_course_headers
from models import Student, Course
from sortStudents import sortStudents

app = Flask(__name__)
app.secret_key = 'some_secret'

# Just saving the location of the uploads to the config dict
app.config['UPLOAD_FOLDER'] = os.path.abspath("uploads")
# Allows extensions used in allowed_file
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])

# Check to see if file has proper extension.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Take in a cell value and the student workbook and return a datetime 
# object representing the date/time value of the cell.
def convert_time(cell_value, student_wb):
    # Used when dates are re
    return datetime(*xlrd.xldate_as_tuple(cell_value, student_wb.datemode))

# Take in a file name and return the file name datestamped.
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.now().strftime(fmt).format(fname=fname)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    form = request.form
    student_data = request.files['student-data']
    course_data = request.files['course-data']
    if (not student_data):
        print("Not found.");
    #print(student_data)

    # Save both student and course data.
    if student_data and allowed_file(student_data.filename):
        student_filename = secure_filename(student_data.filename)
        student_path = os.path.join(app.config['UPLOAD_FOLDER'], student_filename)
        student_data.save(student_path)
    else:
        if not student_data:
            flash("Student data spreadsheet not found, please select and try again.")
        elif not allowed_file(student_data.filename):
            flash("Student data spreadsheet must have extension .xls or .xlsx. Please select the proper spreadsheet and try again.")
        return redirect(url_for('main'))

    if course_data and allowed_file(course_data.filename):
        course_filename = secure_filename(course_data.filename)
        course_path = os.path.join(app.config['UPLOAD_FOLDER'], course_filename)
        course_data.save(course_path)
    else:
        if not course_data:
            flash("Course data spreadsheet not found, please select and try again.")
        elif not allowed_file(course_data.filename):
            flash("Course data spreadsheet must have extension .xls or .xlsx. Please select the proper spreadsheet and try again.")
        return redirect(url_for('main'))

    # Get student/course workbooks
    student_wb = xlrd.open_workbook(filename=student_path)
    course_wb = xlrd.open_workbook(filename=course_path)

    students = []
    student_sheet = student_wb.sheet_by_index(0)
    student_headers = get_student_headers(student_sheet)
    
    # Values that may be blank.
    student_acceptable_blanks = ["pref_one", "pref_two", "pref_three"]
    invalid_students = []
    #print student_headers

    # Take student data from spreadsheet and put into Student objects.
    for i in range(1, student_sheet.nrows):
        invalid_row = False
        student_args = {}
        for name, col in student_headers.iteritems():
            cell_type = student_sheet.cell_type(i, col)
            # Check that blank cells are allowed to be blank.
            if cell_type == xlrd.XL_CELL_EMPTY:
                if name in student_acceptable_blanks:
                    continue
                else:
                    invalid_row = True
                    break
            else:
                value = student_sheet.cell_value(i, col)
                # Do time conversion, see function here
                # https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966#xldate.xldate_as_tuple-function
                if name == "time_submitted":
                    value = convert_time(value, student_wb)

                student_args[name] = value

        if not(invalid_row):
            students.append(Student(**student_args))
        else:
            invalid_students.append(i)

    courses = {}
    course_sheet = course_wb.sheet_by_index(0)
    course_headers = get_course_headers(course_sheet)
    # Values that may be blank.
    course_acceptable_blanks = []
    invalid_courses = []

    for i in range(1, course_sheet.nrows):
        invalid_row = False
        course_args = {}
        for name, col in course_headers.iteritems():
            cell_type = course_sheet.cell_type(i, col)
            if cell_type == xlrd.XL_CELL_EMPTY:
                invalid_row = True
                break
            else:
                course_args[name] = course_sheet.cell_value(i, col)

        if not(invalid_row):
            course = Course(**course_args)
            # Either add seats to existing course, or set course that
            # we haven't seen before.
            try:
                courses[course.getName()].addSeats(course.getSeats())
            except KeyError:
                courses[course.getName()] = course
        else:
            invalid_courses.append(i)

    # For testing, print values of courses.
    #for k, v in courses.iteritems():
    #    print([k])
    #    print(u"Course: {}; Seats: {}".format(v.getName(), v.getSeats()))

    ### UNSORTED STUDENTS ###
    unsorted_students = sortStudents(students, courses)
    u_students_filename = timeStamped("unsorted-students.xls")
    u_students_wb_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        u_students_filename
    )
    # At this point, the courses will have had their arrays filled with students.

    unsorted_students_wb = xlwt.Workbook()
    unsorted_students_sheet = unsorted_students_wb.add_sheet("Students")
    unsorted_student_headers = [
        "ID", "First Name", "Last Name", "First Year Seminar DDB 1", "First Year Seminar DDB 2", "First Year Seminar DDB 3"
    ]
    for index, header in enumerate(unsorted_student_headers):
        unsorted_students_sheet.write(0, index, header)

    for i, student in enumerate(unsorted_students):
        unsorted_students_sheet.write(i + 1, 0, student.getStudentId())
        unsorted_students_sheet.write(i + 1, 1, student.getFName())
        unsorted_students_sheet.write(i + 1, 2, student.getLName())
        prefs = student.getRawPreferences()
        for j, pref in enumerate(prefs):
            unsorted_students_sheet.write(i + 1, j + 3, pref)

    unsorted_students_wb.save(u_students_wb_path)

    ### SORTED STUDENTS ###
    sorted_student_headers = [
        "ID", "First Name", "Last Name", "FSEM Chosen"
    ]
    sorted_students_wb = xlwt.Workbook()
    sorted_students_sheet = sorted_students_wb.add_sheet("Students")
    s_students_filename = timeStamped("sorted-students.xls")
    s_students_wb_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        s_students_filename
    )
    # Create sorted students array
    sorted_students = []
    for course_name, course in courses.iteritems():
        course_students = map(lambda s: (course_name, s), course.getStudents())
        sorted_students.extend(course_students)

    # Add headers to sorted student sheet
    for index, header in enumerate(sorted_student_headers):
        sorted_students_sheet.write(0, index, header)

    for (i, (course_name, student)) in enumerate(sorted_students):
        sorted_students_sheet.write(i + 1, 0, student.getStudentId())
        sorted_students_sheet.write(i + 1, 1, student.getFName())
        sorted_students_sheet.write(i + 1, 2, student.getLName())
        sorted_students_sheet.write(i + 1, 3, course_name)

    sorted_students_wb.save(s_students_wb_path)
    print(s_students_wb_path)

    ### CLOSED COURSES ###
    closed_courses_filename = timeStamped("closed-courses.xls")
    c_courses_wb_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        closed_courses_filename
    )
    closed_courses = [c for (name, c) in courses.iteritems() if c.isFull()]
    closed_course_headers = [
        "Course Name", "Seats"
    ]
    closed_courses_wb = xlwt.Workbook()
    closed_course_sheet = closed_courses_wb.add_sheet("Courses")
    for index, header in enumerate(closed_course_headers):
        closed_course_sheet.write(0, index, header)
    
    for i, course in enumerate(closed_courses):
        closed_course_sheet.write(i + 1, 0, course.getName())
        closed_course_sheet.write(i + 1, 1, course.getSeats())

    closed_courses_wb.save(c_courses_wb_path)

    
    return render_template('results.html', s_path=s_students_filename, us_path=u_students_filename, c_courses=closed_courses_filename)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.debug = True
    app.run()
