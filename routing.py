from flask import Flask, request, redirect, url_for, render_template

import storage.handler_user as handler_user

_INNER_ID_DOCTOR = 'inner_id1'
_INNER_ID_RADIOLOG  = 'inner_id2'
_DUMMY_REQUEST_ID = 1

handler = handler_user.StorageHandler('config.json')

uploaded = False
UPLOAD_FOLDER = 'i:/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/doctor_page', methods=['GET'])
def doctor_page():
    data = handler.get_requests_for_doctor(_INNER_ID_DOCTOR)['requests']
    return render_template('doctor_page.html', data=data)


@app.route('/new_request', methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        pacient_id = request.form['id']
        comment = request.form['comment']
        req_id = handler.create_request(_INNER_ID_DOCTOR, pacient_id, comment)['rid']
        return '''<!doctype html>
                    <h1> Success here's the request id: {}</h1>
                    '''.format(req_id)
                    
    return render_template('newrequest.html')


@app.route('/results', methods=['GET'])
def results():
    results = handler.get_request(_DUMMY_REQUEST_ID)['results']
    keys = list(results.keys())
    data = {
        'patologie{}'.format(i+1): results[keys[i]]['name']
        for i in range(len(keys))
    }
    data.update({
        'scor{}'.format(i+1): results[keys[i]]['yes']
        for i in range(len(keys))
    })
    return render_template('results2.html', data=data)


@app.route('/radiologie', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        request_id = request.form['id']
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_bytes = file.read()

        handler.upload_photo(_INNER_ID_RADIOLOG, request_id, file_bytes)
        return redirect('/')

    return render_template('radiologist_page.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

app.run(debug=True)
