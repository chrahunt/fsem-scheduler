from flask import Flask, flash, render_template, request, redirect, url_for
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
ALLOWED_EXTENSIONS = set(['xlsx'])

# Check to see if file has proper extension.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Take in a cell value and the student workbook and return a datetime 
# object representing the date/time value of the cell.
def convert_time(cell_value, student_wb):
    # Used when dates are re
    return datetime(*xlrd.xldate_as_tuple(cell_value, student_wb.datemode))

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    form = request.form
    student_data = request.files['student-data']
    course_data = request.files['course-data']

    # Save both student and course data.
    if student_data and allowed_file(student_data.filename):
        student_filename = secure_filename(student_data.filename)
        student_path = os.path.join(app.config['UPLOAD_FOLDER'], student_filename)
        student_data.save(student_path)
    else:
        flash("Please try again.")
        return redirect(url_for('main'))

    if course_data and allowed_file(course_data.filename):
        course_filename = secure_filename(course_data.filename)
        course_path = os.path.join(app.config['UPLOAD_FOLDER'], course_filename)
        course_data.save(course_path)
    else:
        flash("Please try again.")
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
    for k, v in courses.iteritems():
        print([k])
        print(u"Course: {}; Seats: {}".format(v.getName(), v.getSeats()))

    unsorted_students = sortStudents(students, courses)
    print len(unsorted_students)
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
