import os
from depth_groundwather import DepthGroundWather
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
            response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

@app.route('/drastic/d', methods=['GET', 'POST'])
def calculate_d():
    if request.method == 'POST':
        data = request.data
        input_mdt = "/home/rodrigo/data/d/input/d.sdat"
        max_depth = 20
        distance = 200
        min_size = 50
        ratings = [0.0, 1.5, 10.0,  1.5, 4.6, 9.0,  4.6, 9.1, 7.0,  9.1, 15.2, 5.0,  15.2, 22.9, 3.0,  22.9, 30.5, 2.0,  30.5, 200.0, 1.0]
        output_path = "/home/rodrigo/data/d/result/d.tif"
        depth = DepthGroundWather()
        depth.convert_mdt(input_mdt, max_depth, distance, min_size, ratings, output_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
