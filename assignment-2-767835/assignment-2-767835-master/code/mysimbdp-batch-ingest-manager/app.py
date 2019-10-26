import os
import json

from flask import Flask, url_for, redirect, request, render_template
import pandas as pd
import requests
import http.client



app=Flask(__name__)


@app.route("/set_data_management_function", methods=["POST"])
def set_data_management_function():
    res={
            "status": "",
            "motive": "",
            "request": "/set_data_management_function",
            "result": ""
        }
    customer=request.form['customer_identifier']
    #we get the funtion as text
    function=request.form['treatment_function']
    try:
        #response=request.post(url="http://coredms-service/set_data_management_function", data={"function": function, "customer_identifier": customer})
        connexion=http.client.HTTPConnection("coredms-service", 30002)
        data={
                    "customer_identifier": customer
                }
        headers={"Content-type": "application/json"}
        connexion.request('POST', '/set_data_management_function', json.dumps(data), headers)

        response=connexion.getresponse()
        response=response['data']
        connexion.close()

        response=response.read().decode()

    except HttpError as httperr:
        res['status']="failure"
        res['motive']="HttpError: "+str(httperr)
        return res
    except Exception as err:
        res['status']="failure"
        res['motive']="Exception: "+str(err)

    response=response.text
    response=json.loads(response)
    res['status']=response['status']
    res['motive']=response['motive']
    res['result']=response['result']
    return res





@app.route("/get_list_of_files", methods=["POST"])
def get_list_of_files():

    res={
            "status": "",
            "motive": "",
            "request": "/get_list_of_files",
            "result": ""
        }
    customer=request.form['customer_identifier']
    try:
        connexion=http.client.HTTPConnection("coredms-service", 30002)
        data={
                    "customer_identifier": customer
                }
        headers={"Content-type": "application/json"}
        connexion.request('POST', '/get_all_my_files', json.dumps(data), headers)

        response=connexion.getresponse()
        connexion.close()

        response=response.read().decode()


    except HttpError as err:
        res['status']="failure"
        res['motive']="HttpError: "+str(err)
        return res
    except Exception as err:
        res['status']="failure"
        res['motive']="Exception: "+str(err)
        return res
    response=response['data']
    res["status"]=response['status']
    res["motive"]=response['motive']
    res['result']=response['result']
    return json.dumps(res)





@app.route('/execute_ingestion', methods=["POST"])
def execute_ingestion():
    #on recupere le customer
    customer=request.form['customer_identifier']

    #on recupere le texte de la fonction, et on la met dans un fichier

    #on recupère la liste des fichier depuis la bdd, on cree les fichiers

    #on execute la fonction sur chaque fichier, en inserant le resultat dans la bdd


    #on retourne la valeur succes

















app.run(host="0.0.0.0", port=80, debug=True)
