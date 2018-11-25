import os
from flask import Flask, request, redirect, url_for, render_template
from threading import Thread
from multiprocessing.pool import ThreadPool
import subprocess
from check_one import predict
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



@app.route('/results', methods=['GET'])
def results():
			return render_template('result2.html', pat1=l1[0] , pat2=l2[0] ,scor1=l1[1] , scor2=l2[1] )

@app.route('/radiologie', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded = True
            return redirect(url_for('results', path=path))
    return render_template('index.html')
app.run(debug=True)
