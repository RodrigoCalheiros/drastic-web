import os
import settings

from flask import Flask, flash, request, redirect, url_for, Response

from depth_groundwather.depth_groundwather import DepthGroundWather
from file.file import File

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = settings.DRASTIC_DATA_FOLDER_D_INPUT

@app.route('/drastic/d/upload/mdt', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            response = Response("{'msg': 'No file part'", status=403, mimetype='application/json')
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        request_file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if request_file.filename == '':
            flash('No selected file')      
            response = Response("{'msg': 'No selected file'", status=403, mimetype='application/json')
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        file = File()
        if request_file and file.allowed_file(request_file.filename, settings.ALLOWED_EXTENSIONS):
            file.save(request_file, app.config['UPLOAD_FOLDER'])
            response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

@app.route('/drastic/d/calculate', methods=['POST'])
def calculate_d():
    if request.method == 'POST':
        print request.data
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
