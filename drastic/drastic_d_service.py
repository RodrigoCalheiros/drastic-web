import os
from flask import Flask, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/home/rodrigo/data/d"
ALLOWED_EXTENSIONS = {'txt', 'prj', 'sdat', 'sgrd'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/drastic/mdt', methods = ['POST'])
def upload_file_mdt():
    return "depth"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/drastic/d/mdt', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return Response("{'msg': 'No file part'", status=403, mimetype='application/json')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return Response("{'msg': 'No selected file'", status=403, mimetype='application/json')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return Response("{'msg': 'Sucess'", status=200, mimetype='application/json')

@app.route('/drastic/d', methods=['GET', 'POST'])
def calculate_d():
    if request.method == 'POST':
        data = request.data
        print(data)
    return Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
