#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 23:17:28 2020

@author: ishmeet
"""


from flask import Flask, jsonify, request, make_response

app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found2(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/healthcheck', methods = ['GET'])
def healthcheck():
    healthcheck = {
        'healthcheck': "OK"
    }
    return jsonify( healthcheck ), 200

@app.route('/SaveRow', methods = ['POST', 'GET'])
def saveRecord():
    if request.method == 'POST':
        print("request.json:",request.json)
        print("request: ",request.form)
        name = request.form.get('name')
        
        #return '''<h1>Thank you {}</h1>'''.format(name)
        return '''<script>alert("Thank you {}");window.location.href = "index.html";</script>'''.format(name)
        
    response = {
        'Response': "OK"
    }
    return jsonify( response ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')