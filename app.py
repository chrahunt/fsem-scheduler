from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import xlrd, xlwt
import os
from datetime import datetime

from parse import get_student_headers, get_course_headers, HeaderError
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
    # Make upload directory if needed.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

    form = request.form
    student_data = request.files['student-data']
    course_data = request.files['course-data']

    # Save spreadsheets locally.
    if student_data and allowed_file(student_data.filename):
        student_filename = secure_filename(student_data.filename)
        student_path = os.path.join(app.config['UPLOAD_FOLDER'], student_filename)
        student_data.save(student_path)
    else:
        # Error handling: No spreadsheet uploaded or wrong file extension for student sheet.
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
        # Error handling: No spreadsheet uploaded or wrong file extension for course sheet.
        if not course_data:
            flash("Course data spreadsheet not found, please select and try again.")
        elif not allowed_file(course_data.filename):
            flash("Course data spreadsheet must have extension .xls or .xlsx. Please select the proper spreadsheet and try again.")
        return redirect(url_for('main'))

    # Check to make sure the files were saved.
    if not os.path.isfile(student_path):
        flash("Error saving Student spreadsheet. Please try again.")

    if not os.path.isfile(course_path):
        flash("Error saving Course spreadsheet. Please try again.")

    # Load workbooks into XLRD workbook objects.
    try:
        student_wb = xlrd.open_workbook(filename=student_path)
    except xlrd.XLRDError:
        # Error handling: xlrd error opening student workbook.
        flash("Student spreadsheet formatted incorrectly. Please try again.")
        return redirect(url_for('main'))

    try:
        course_wb = xlrd.open_workbook(filename=course_path)
    except xlrd.XLRDError:
        # Error handling: xlrd error opening course workbook.
        flash("Course spreadsheet formatted incorrectly. Please try again.")
        return redirect(url_for('main'))

    # Error handling: Check that both the workbooks have at least 1 sheet.
    if (student_wb.nsheets == 0):
        flash("Student spreadsheet does not contain any sheets. Please correct and try again.")
        return redirect(url_for('main'))

    if (course_wb.nsheets == 0):
        flash("Course spreadsheet does not contain any sheets. Please correct and try again.")
        return redirect(url_for('main'))

    # Retrieve the columns corresponding the headers for each sheet.
    student_sheet = student_wb.sheet_by_index(0)
    try:
        student_headers = get_student_headers(student_sheet)
    except HeaderError as e:
        # Error handling: Some headers were not found in the student sheet.
        missing_headers = e.get_headers()
        missing_header_list = reduce(lambda text, header: "{}, \"{}\"".format(text, header), missing_headers[1:], "\"{}\"".format(missing_headers[0]))
        flash("Student spreadsheet does not have the following header{}: {}".format("s" if len(missing_headers) > 1 else "", missing_header_list))
        return redirect(url_for('main'))
    
    course_sheet = course_wb.sheet_by_index(0)
    try:
        course_headers = get_course_headers(course_sheet)
    except HeaderError as e:
        # Error handling: Some headers were not found in the course sheet.
        missing_headers = e.get_headers()
        missing_header_list = reduce(lambda text, header: "{}, \"{}\"".format(text, header), missing_headers[1:], "\"{}\"".format(missing_headers[0]))
        flash("Course spreadsheet does not have the following header{}: {}".format("s" if len(missing_headers) > 1 else "", missing_header_list))
        return redirect(url_for('main'))
    
    # Put data from sheet into objects.
    # Values that may be blank for each row.
    student_acceptable_blanks = ["pref_one", "pref_two", "pref_three"]
    students = []
    invalid_students = []

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
            # Student was mising a column they needed.
            invalid_students.append(i)

    courses = {}
    
    # Values that may be blank.
    course_acceptable_blanks = []
    invalid_courses = []

    # Put course information into course object.
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

    # Do allocation of students, returns unsorted students and courses that were
    # not found, and also inserts students into the students list in each course
    unsorted_students, missing_courses = sortStudents(students, courses)
    # At this point,  courses will have had their arrays filled with students.
    
    ### UNSORTED STUDENTS ###
    u_students_filename = timeStamped("unsorted-students.xls")
    u_students_wb_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        u_students_filename
    )

    # Construct workbooks and populate them.
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
        "Course Name", "Seats", "Requests"
    ]
    closed_courses_wb = xlwt.Workbook()
    closed_course_sheet = closed_courses_wb.add_sheet("Courses")
    for index, header in enumerate(closed_course_headers):
        closed_course_sheet.write(0, index, header)
    
    for i, course in enumerate(closed_courses):
        closed_course_sheet.write(i + 1, 0, course.getName())
        closed_course_sheet.write(i + 1, 1, course.getSeats())
        closed_course_sheet.write(i + 1, 2, course.getRequests())

    closed_courses_wb.save(c_courses_wb_path)
    
    # Inform about rows with invalid students.
    if (invalid_students):
        invalid_student_list = ', '.join([str(x) for x in invalid_students])
        flash("The following row{} in the Student spreadsheet were missing necessary values: {}".format('s' if len(invalid_students) > 1 else "", invalid_student_list))

    # Inform about requests made for missing courses.
    if (missing_courses):
        invalid_courses_list = '; '.join(["{} ({})".format(k, len(v)) for k, v in missing_courses.iteritems()])
        flash("The following course{} requested but not found in the course spreadsheet (number of times requested listed): {}".format('s were' if len(missing_courses) > 1 else ' was', invalid_courses_list))

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
