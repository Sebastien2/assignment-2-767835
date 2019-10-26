import os
import json
import pandas as pd
import requests
from flask import Flask, redirect, url_for, request, render_template


app=Flask(__name__)


@app.route("/add_customer", method=["POST"])
def add_customer():
    customer_identifier=request.form['customer_identifier']
    #and then we send the request to coredms
    try:
        response=requests.post(url='http://coredms-service/add_customer', data={"customer_identifier": customer_identifier})
        
    except HttpError as http_err:
        return "HTTP error:" + str(http_err)
    except Exception as err:
        return "Error occcured:" + str(err)
    response=response.text
    args=json.loads(response)
    return json.dumps(args)



@app.route("/get_customer", method=["POST"])
def get_customer():
    customer_identifier=request.form['customer_identifier']
    #and then we send the request to coredms
    try:
        response=requests.post(url='http://coredms-service/get_customer', data={"customer_identifier": customer_identifier})
        
    except HttpError as http_err:
        return "HTTP error:" + str(http_err)
    except Exception as err:
        return "Error occcured:" + str(err)
    response=response.text
    args=json.loads(response)
    return json.dumps(args)



app.run(host="0.0.0.0", port=80, debug=True)

