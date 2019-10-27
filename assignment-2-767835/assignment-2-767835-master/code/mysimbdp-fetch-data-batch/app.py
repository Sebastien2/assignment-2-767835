import os
import json
import pandas as pd

from flask import Flask, url_for, redirect, request, render_template, flash

import http.client

UPLOAD_FOLDER="/files/"
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
        fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], customer+"_data_file_"+filename))
        flash('File successfully uploaded')
    
    return json.dumps({
                    "status": "success",
                    "motive": "",
                    "request": "add_data_file",
                    "result": "filename"
                     })




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




#functions that are for ingestion of the data
@app.route("/set_data_management_function", methods=["POST"])
def set_data_management_function():
    res={
            "status": "",
            "motive": "",
            "request": "set_data_management_function",
            "result": ""
        }
    customer=request.form['customer_identifier']
    function=request.form['function']
    filename=customer+"_ingestion_function.py"
    with open("/files/"+filename, "w") as f:
        f.write(function)
        f.close()
        res['status']="success"
        res['result']="file created: " + filename
    return json.dumps(res)


@app.route("/get_list_of_files", methods=["POST"])
def get_list_of_files():
    res={
            "status": "",
            "motive": "",
            "resquest": "get_list_of_files",
            "result": ""
        }
    customer=requst.form['customer_identifier']
    #then we get all the files that start with <customer>_data_file_

    filenames=[]
    for fname in os.listdir(path="/files/"):
        if customer+"_data_file" in fname:
            #we get the file
            filenames.append("/files/"+fname)

    res['result']=str(filenames)

    return json.dumps(res)


@app.route("/execute_ingestion", methods=["POST"])
def execute_ingestion():
    res={
            "status": "",
            "motive": "",
            "request": "execute_ingestion",
            "result": ""
        }
    customer=request.form['customer_identifier']

    #and we get the list of the files of data
    filenames=[]
    for fname in os.listdir(path="/files/"):
        if customer+"_data_file" in fname:
            #we get the file
            filenames.append("/files/"+fname)


    #we get the file with the function
    execution_filename="/files/"+customer+"_ingestion_function.py"

    #TODO: execute the function on each file

    #we ingest the data
    for data_filename in filenames:
        execute_ingestion_of_data_in_database(data_filename, customer)

    res["status"]="success"
    res["result"]="data  ingested for "+len(filenames) + "data files"
    return json.dumps(res)





def execute_ingestion_of_data_in_database(filename, customer):
    #we open the file, and send the content over to coredms for insertion
    with open(filename, "r") as f:
        content=f.read()
        f.close()
    try:
        connexion=http.client.HTTPConnection("coredms-service", 30002)
        data={
                "customer_identifier": customer,
                "data": content
            }
        headers={"Content-type": "application/json"}
        connexion.request('POST', "/add_many_data", json.dumps(data), headers)
        response=connexion.getresponse()
        response=response['data']
        connexion.close()

    return




app.run(host="0.0.0.0", port=80, debug=True)

