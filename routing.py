import os
from flask import Flask, request, redirect, url_for, render_template
from threading import Thread
from multiprocessing.pool import ThreadPool
import subprocess
from werkzeug.utils import secure_filename

uploaded = False
UPLOAD_FOLDER = 'i:/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

           
data = [{'Nume':"Ion Ionescu", 'CNP':"1234567890", 'link':"http://example.com"}]

@app.route('/doctor_page', methods=['GET'])
def doctor_page():
            return render_template('doctor_page.html', data=data )

@app.route('/new_request', methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        pacient_name = request.form['name']
        pacient_cnp = request.form['cnp']
        print(pacient_cnp, pacient_name)
        return '''<!doctype html>
                    <h1> Success here's your patient ID </h1>
                    '''
                    
    return render_template('newrequest.html')

@app.route('/results', methods=['GET'])
def results():
            return render_template('results2.html')

@app.route('/radiologie', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        pacient_id = request.form['id']
        pacient_comment = request.form['comment']
        print(pacient_comment, pacient_id)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_bytes = file.read()
            print(file_bytes)
        return redirect('/')

    return render_template('radiologist_page.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

app.run(debug=True)
