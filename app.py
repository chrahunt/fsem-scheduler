from flask import Flask, render_template, request, redirect, url_for
import xlrd

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        student_data = request.files['student-data']
        class_data = request.files['class-data']
	if student_data and allowed_file(student_data.filename):
		filename = secure_filename(student_data.filename)
		student_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	if class_data and allowed_file(class_data.filename):
		filename2 = secure_filename(class_data.filename)
		class_data.save(ox.path.join(app.config['UPLOAD_FOLDER'], filename2))
    except KeyError:
        # One or both of the files was not provided, redirect back to the main page folder now
        return redirect(url_for('main'))
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
