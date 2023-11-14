#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask,send_from_directory, request, jsonify, make_response, render_template

import requests as req

from constants import *

app = Flask(__name__)

#==========================================================
#============= SERVER API =================================
#==========================================================

# Example of List
@app.route('/getList',methods = ['GET'])
def getList():

  try:

    print('Estoy dentro')

    return make_response(jsonify({ "data" : "Respuesta obtenida"}), 200)
    
  except Exception as ex:
    print('ERROR: ',ex.args)

# Method to retrieve satellite images
@app.route('/postExample',methods = ['POST'])
def postExample():
  try:
    #Recover the body (JSON)
    body = request.get_json()

    #Property organization is mandatory
    if "name" in body:
      name = body['name']
      print('\nName: ', name)
    else:
      print('\nProperty name is mandatory')
      return make_response(jsonify({ "data" : 'Property name is mandatory'}), 400)

    return make_response(jsonify({ "data" : "Properties received"}), 200)

  except Exception as ex:
    print('Error postExample method (script.py): ', ex.args)
    print(ex)

  return make_response(jsonify({ "data" : "Error during the execution"}), 400)

if __name__ == '__main__':
  #Run the API
  app.run(host= HOST, port = PORT, threaded = True, debug = True, use_reloader = False)
