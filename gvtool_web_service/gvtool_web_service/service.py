import os
import settings
import json

from flask import Flask, flash, request, redirect, url_for, Response
from file.file import File

from drastic.depth_groundwather.depth_groundwather import DepthGroundWather
from drastic.recharge.recharge import Recharge
from drastic.aquifer.aquifer import Aquifer
from drastic.soil_media.soil_media import SoilMedia
from drastic.topography.topography import Topography
from drastic.impact_zone.impact_zone import ImpactZone
from drastic.hidraulic_conductivity.hidraulic_conductivity import HidraulicConductivity
from drastic.drastic import Drastic

from god.depth_groundwater.depth_groundwater import GodDepthGroundWater
from god.overall_lithology.overall_lithology import OverallLithology
from god.groundwater_occurrence.groundwater_occurrence import GroundwaterOccurrence
from god.god import God



from shp.shp import Shp
from pprint import pprint

app = Flask(__name__)

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

@app.route('/drastic/shp/header/<variable>', methods=['GET'])
def get_shp_header(variable):
    header = []
    if request.method == 'GET':

        if variable == 'a':
            input_file = settings.DRASTIC_DATA_FOLDER_A_INPUT + "a.shp"
        elif variable == 's':
            input_file = settings.DRASTIC_DATA_FOLDER_S_INPUT + "s.shp"

        shp = Shp(input_file)
        header = shp.get_header()

    dataresponse =  {"msg": "Sucess", "data": header }
    response = Response(json.dumps(dataresponse), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/shp/value/<variable>', methods=['GET'])
def get_shp_value(variable):
    if request.method == 'GET':

        if variable == 'a':
            input_file = settings.DRASTIC_DATA_FOLDER_A_INPUT + "a.shp"
        elif variable == 's':
            input_file = settings.DRASTIC_DATA_FOLDER_S_INPUT + "s.shp"

        field = request.args.get("field")
        shp = Shp(input_file)
        values = shp.get_values(field)
    dataresponse =  {"msg": "Sucess", "data": values }
    response = Response(json.dumps(dataresponse), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/d/calculate', methods=['POST'])
def calculate_d():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_D_INPUT + "d.sdat"
        process_path = settings.DRASTIC_DATA_FOLDER_D_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_D_RESULT + "d.tif"
        data =  json.loads(request.form["data"])
        max_depth = data["maxDepth"]
        distance = data["distance"]
        min_size = data["minSize"]
        ratings = data["ratings"]
        depth = DepthGroundWather(input_file, output_file, max_depth, distance, min_size, ratings)
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
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        recharge = Recharge(input_file, output_file, ratings)
        recharge.convert_mdt(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/a/calculate', methods=['POST'])
def calculate_a():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_A_INPUT + "a.shp"
        process_path = settings.DRASTIC_DATA_FOLDER_A_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_A_RESULT + "a.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        field = data["field"]
        aquifer = Aquifer(input_file, output_file, 30, field, ratings)
        aquifer.convert_mdt(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/s/calculate', methods=['POST'])
def calculate_s():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_S_INPUT + "s.shp"
        process_path = settings.DRASTIC_DATA_FOLDER_S_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_S_RESULT + "s.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        field = data["field"]
        soil_media = SoilMedia(input_file, output_file, 30, field, ratings)
        soil_media.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/t/calculate', methods=['POST'])
def calculate_t():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_T_INPUT + "t.sdat"
        process_path = settings.DRASTIC_DATA_FOLDER_T_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_T_RESULT + "t.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        topography = Topography(input_file, output_file, 30, ratings)
        topography.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/i/calculate', methods=['POST'])
def calculate_i():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_I_INPUT + "i.shp"
        process_path = settings.DRASTIC_DATA_FOLDER_I_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_I_RESULT + "i.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        field = data["field"]
        impact_zone = ImpactZone(input_file, output_file, 30, field, ratings)
        impact_zone.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/c/calculate', methods=['POST'])
def calculate_c():
    if request.method == 'POST':
        input_file = settings.DRASTIC_DATA_FOLDER_C_INPUT + "c.shp"
        process_path = settings.DRASTIC_DATA_FOLDER_C_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_C_RESULT + "c.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        field = data["field"]
        hidraulic_conductivity = HidraulicConductivity(input_file, output_file, 30, field, ratings)
        hidraulic_conductivity.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drastic/drastic/calculate', methods=['POST'])
def calculate_drastic():
    if request.method == 'POST':
        input_file_d = settings.DRASTIC_DATA_FOLDER_D_RESULT + "d.tif"
        input_file_r = settings.DRASTIC_DATA_FOLDER_R_RESULT + "r.tif"
        input_file_a = settings.DRASTIC_DATA_FOLDER_A_RESULT + "a.tif"
        input_file_s = settings.DRASTIC_DATA_FOLDER_S_RESULT + "s.tif"
        input_file_t = settings.DRASTIC_DATA_FOLDER_T_RESULT + "t.tif"
        input_file_i = settings.DRASTIC_DATA_FOLDER_I_RESULT + "i.tif"
        input_file_c = settings.DRASTIC_DATA_FOLDER_C_RESULT + "c.tif"
        process_path = settings.DRASTIC_DATA_FOLDER_DRASTIC_PROCESS
        output_file = settings.DRASTIC_DATA_FOLDER_DRASTIC_RESULT + "drastic.tif"

        data =  json.loads(request.form["data"])
        weight_d = data["weight_d"]
        weight_r = data["weight_r"]
        weight_a = data["weight_a"]
        weight_s = data["weight_s"]
        weight_t = data["weight_t"]
        weight_i = data["weight_i"]
        weight_c = data["weight_c"]

        drastic = Drastic(input_file_d, input_file_r, input_file_a, input_file_s, input_file_t, input_file_i, input_file_c, weight_d, weight_r, weight_a, weight_s, weight_t, weight_i, weight_c, output_file, 30)
        drastic.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/god/g/calculate', methods=['POST'])
def calculate_god_g():
    if request.method == 'POST':
        input_file = settings.GOD_DATA_FOLDER_G_INPUT + "g.shp"
        process_path = settings.GOD_DATA_FOLDER_G_PROCESS
        output_file = settings.GOD_DATA_FOLDER_G_RESULT + "g.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        field = data["field"]
        groundwater_occurrence = GroundwaterOccurrence(input_file, output_file, 30, field, ratings)
        groundwater_occurrence.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/god/o/calculate', methods=['POST'])
def calculate_god_o():
    if request.method == 'POST':
        input_file = settings.GOD_DATA_FOLDER_O_INPUT + "o.shp"
        process_path = settings.GOD_DATA_FOLDER_O_PROCESS
        output_file = settings.GOD_DATA_FOLDER_O_RESULT + "o.tif"
        data =  json.loads(request.form["data"])
        ratings = data["ratings"]
        field = data["field"]
        overall_lithology = OverallLithology(input_file, output_file, 30, field, ratings)
        overall_lithology.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/god/d/calculate', methods=['POST'])
def calculate_god_d():
    if request.method == 'POST':
        input_file = settings.GOD_DATA_FOLDER_D_INPUT + "d.sdat"
        process_path = settings.GOD_DATA_FOLDER_D_PROCESS
        output_file = settings.GOD_DATA_FOLDER_D_RESULT + "d.tif"
        data =  json.loads(request.form["data"])
        max_depth = data["maxDepth"]
        distance = data["distance"]
        min_size = data["minSize"]
        ratings = data["ratings"]
        depth = GodDepthGroundWater(input_file, output_file, max_depth, distance, min_size, ratings)
        depth.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/god/god/calculate', methods=['POST'])
def calculate_god():
    if request.method == 'POST':
        input_file_g = settings.GOD_DATA_FOLDER_G_RESULT + "g.tif"
        input_file_o = settings.GOD_DATA_FOLDER_O_RESULT + "o.tif"
        input_file_d = settings.GOD_DATA_FOLDER_D_RESULT + "d.tif"
        process_path = settings.GOD_DATA_FOLDER_GOD_PROCESS
        output_file = settings.GOD_DATA_FOLDER_GOD_RESULT + "god.tif"

        god = God(input_file_g, input_file_o, input_file_d, output_file, 30)
        god.calculate(process_path)
    response = Response("{'msg': 'Sucess'", status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response