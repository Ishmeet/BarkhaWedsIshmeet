#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 23:17:28 2020

@author: ishmeet
"""


from flask import Flask, jsonify, request, make_response
import csv
import smtplib
import ssl
import mimetypes
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart



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
    print("METHOD: ", request.method)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        option = request.form.get('option')
        print(name, email, option)        
        with open('guests.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, option])
        
        #msg = EmailMessage()
        #msg['Subject'] = 'barkhawedsishmeet.in guests list'
        #msg['from'] = 'ishmeet.bhamra.2016@gmail.com'
        #msg['To'] = 'ishmeetsinghis@gmail.com'
        msg = MIMEMultipart()
        msg["From"] = 'ishmeet.bhamra.2016@gmail.com'
        msg["To"] = 'ishmeetsinghis@gmail.com,barkhaflora92@gmail.com'
        msg["Subject"] = "Barkha Weds Ishmeet New Notification"
        msg.preamble = "Barkha Weds Ishmeet New Notification"
        
        
        _DEFAULT_CIPHERS = (
'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
'!eNULL:!MD5')
        
        #smtp_server = smtplib.SMTP('smtp.gmail.com', port=587)
        
        # only TLSv1 or higher
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        
        context.set_ciphers(_DEFAULT_CIPHERS)
        context.set_default_verify_paths()
        context.verify_mode = ssl.CERT_REQUIRED
        
        #if smtp_server.starttls(context=context)[0] != 220:
        #    return False # cancel if connection is not encrypted
        #smtp_server.login('ishmeet.bhamra.2016@gmail.com', 'Mxygtwxas@2')
        #smtp_server.starttls(context=context)
        
        with open('guests.csv', 'rb') as fp:
            #csv_data = fp.read()
            ctype, encoding = mimetypes.guess_type('guests.csv')            
            maintype, subtype = ctype.split("/", 1)
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename='guests.csv')
            msg.attach(attachment)
            #msg.add_attachment(csv_data, maintype='application', subtype='octet-stream')
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls(context=context)
            s.ehlo
            s.login('ishmeet.bhamra.2016@gmail.com', 'Mxygtwxas#3')
            s.send_message(msg)
            s.quit()
        
        #return '''<h1>Thank you {}</h1>'''.format(name)
        return '''<script>alert("Thank you {}");window.location.href = "index.html";</script>'''.format(name)
        
    response = {
        'Response': "OK"
    }
    return jsonify( response ), 200

@app.route('/index.html', methods = ['GET'])
def index():
    return '''<h1><a href="https://barkhawedsishmeet.in">Go Back</a></h1>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
