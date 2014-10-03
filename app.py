from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        student_data = request.files['student-data']
        class_data = request.files['class-data']
    except KeyError:
        # One or both of the files was not provided, redirect back to the main page for now
        return redirect(url_for('main'))
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.debug = True
    app.run()