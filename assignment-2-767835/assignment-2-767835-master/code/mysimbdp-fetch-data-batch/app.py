import os
import json
import pandas as pd

from flask import Flask, url_for, redirect, request, render_template, flash

import http.client

UPLOAD_FOLDER="./uploads"
app=Flask(__name__)
app.secret_key="secret_key"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=100*1024*1024  # 100 Mb as max size

ALLOWED_EXTENSIONS=["json"]






@app.route("/get_constraints", methods=["POST"])
def get_constraints():
    constraints=""
    with open("constraints.yaml", "r") as constraints:
        constraints=constraints.read()
    res={
            "status": "success",
            "motive" : "",
            "request": "get_constraints",
            "result": constraints
        }
    return json.dumps(res)





@app.route("/add_data_file", method=["POST"])
def add_data_file():
    #we get the customer name
    customer=request.form['customer_identifier']
    #we get the file
    if 'file' not in request.files:
        flash('No file part')
        return rediret(request.url)
    fichier=request.files['file']
    if fichier.filename=='':
        flash('No file selected for uplaoding')
        return redirect(request.url)
    if fichier and allowed_file(fichier.filename):
        filename=secure_filename(fichier.filename)
        fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], customer+"_"+filename))
        flash('File successfully uploaded')
        return redirect(request.url)
    #we senf the file 
    #TODO: send the file to MongoDB in case we can't get it from all instances
    #the files will not be accessible to all instances, so we put it in mongdb -> what was doene above is useless
    #we use the variables fichier and filename
    with open(os.path(join(app.config['UPLOAD_FOLDER'], customer+"_"+filename)) as f:
        try:
            connexion=http.client.HTTPConnection('coredms-service', 30002)
            headers={"Content-type": "application/json"}
            data={
                    "customer_identifier": customer,
                    "filename": customer+"_"+filename,
                    "file": f.read()
                }
            data=json.dumps(data)
            connexion.request('POST', "/add_file", data, headers)
            response=connexion.getresponse()
            connexion.close()

            #response=requests.post("http://coredms-service/add_file", data={"customer_identifier": customer, "filename": customer+"_"filename, "file": f.read() })
        except HttpError as err:
            return json.dumps({
                                    "status": "failure",
                                    "motive": "HttpError: "+str(err),
                                    "request": "add_data_file",
                                    "result": ""
                                })
        except Exception as error:
            return json.dumps({
                                    "status": "failure",
                                    "motive": "Exception: "+str(error),
                                    "request": "add_data_file",
                                    "result": ""
                                })
    
    return json.dumps({
                    "status": "success",
                    "motive": "",
                    "request": "add_data_file",
                    "result": "filename"
                     })




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app.run(host="0.0.0.0", port=80, debug=True)

