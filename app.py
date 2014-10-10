from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug import secure_filename
import xlrd, xlwt
import os

from parse import get_student_headers

app = Flask(__name__)
app.secret_key = 'some_secret'

# Just saving the location of the uploads to the config dict
app.config['UPLOAD_FOLDER'] = os.path.abspath("uploads")
# Allows extensions used in allowed_file
ALLOWED_EXTENSIONS = set(['xlsx'])

# Check to see if file has proper extension.
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

    student_sheet = student_wb.sheet_by_index(0)    

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
