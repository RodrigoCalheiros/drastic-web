import os
import settings
import json

from flask import Flask, flash, request, redirect, url_for, Response
from file.file import File
from depth_groundwather.depth_groundwather import DepthGroundWather
from aquifer.aquifer import Aquifer
from recharge.recharge import Recharge
from shp.shp import Shp
from pprint import pprint




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = settings.DRASTIC_DATA_FOLDER_D_INPUT

@app.route('/drastic/upload/<variable>', methods=['POST'])
def upload_file(variable):
    if request.method == 'POST':
        print(request.files)
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
        
        file = File(request_file)
        #file.unzip(settings.DRASTIC_DATA_FOLDER_D_INPUT)
        #response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
        #response.headers.add('Access-Control-Allow-Origin', '*')
        #return response

        if request_file and file.allowed_file(settings.ALLOWED_EXTENSIONS):
            if variable == 'd':
                file.save(settings.DRASTIC_DATA_FOLDER_D_INPUT, variable)
            elif variable == 'r':
                file.save(settings.DRASTIC_DATA_FOLDER_R_INPUT, variable)
            elif variable == 'a':
                file.save(settings.DRASTIC_DATA_FOLDER_A_INPUT, variable)
            elif variable == 's':
                file.save(settings.DRASTIC_DATA_FOLDER_S_INPUT, variable)
            elif variable == 't':
                file.save(settings.DRASTIC_DATA_FOLDER_T_INPUT, variable)
            elif variable == 'i':
                file.save(settings.DRASTIC_DATA_FOLDER_I_INPUT, variable)
            elif variable == 'c':
                file.save(settings.DRASTIC_DATA_FOLDER_C_INPUT, variable)
            response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

@app.route('/drastic/d/calculate', methods=['POST'])
def calculate_d():
    if request.method == 'POST':
        data =  json.loads(request.form["data"])
        input_file = settings.DRASTIC_DATA_FOLDER_D_INPUT + "d.sdat"
        process_path = settings.DRASTIC_DATA_FOLDER_D_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_D_RESULT + "d.tif"
        max_depth = data["maxDepth"]
        distance = data["distance"]
        min_size = data["minSize"]
        rattings = settings.D_RATINGS
        depth = DepthGroundWather(input_file, output_file, max_depth, distance, min_size, rattings)
        depth.convert_mdt(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/drastic/r/calculate', methods=['POST'])
def calculate_r():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_R_INPUT + "r.sdat"
        process_path = settings.DRASTIC_DATA_FOLDER_R_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_R_RESULT + "r.tif"
        rattings = settings.R_RATINGS
        recharge = Recharge(input_file, output_file, rattings)
        recharge.convert_mdt(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/a/calculate', methods=['POST'])
def calculate_a():
    if request.method == 'POST':
        data =  json.loads(request.form["data"])
        print(data)
        input_file = settings.DRASTIC_DATA_FOLDER_A_INPUT + "a.shp"
        process_path = settings.DRASTIC_DATA_FOLDER_A_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_A_RESULT + "a.tif"
        rattings = settings.A_RATINGS
        aquifer = Aquifer(input_file, output_file, 30, "dd", rattings)
        aquifer.convert_mdt(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/shp/header/<variable>', methods=['GET'])
def get_shp_header(variable):
    header = []
    if request.method == 'GET':
        print(variable)
        input_file = settings.DRASTIC_DATA_FOLDER_A_INPUT + "a.shp"
        shp = Shp(input_file)
        header = shp.get_header()
    dataresponse =  {"msg": "Sucess", "data": header }
    response = Response(json.dumps(dataresponse), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/shp/value/<variable>', methods=['GET'])
def get_shp_value(variable):
    if request.method == 'GET':
        field = request.args.get("field")
        input_file = settings.DRASTIC_DATA_FOLDER_A_INPUT + "a.shp"
        shp = Shp(input_file)
        values = shp.get_values(field)
    dataresponse =  {"msg": "Sucess", "data": values }
    response = Response(json.dumps(dataresponse), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response