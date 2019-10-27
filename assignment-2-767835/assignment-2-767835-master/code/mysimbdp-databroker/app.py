import os
import json

import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
import pika

app=Flask(__name__)


connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-service', 30015))
channel=connection.channel()
#channel.queue_declare("queue")



@app.route("/get_format_message_specification", methods=["POST"])
def get_format_message_specification():
    res={
            "status": "success",
            "motive": "",
            "request": "get_format_message_specification",
            "result": ""
        }
    
    specification=""
    with open("format_message_specification.txt") as f:
        specification=f.read()
        f.close()
        res['result']=specification
    return json.dumps(res)





@app.route("/add_message", methods=["POST"])
def add_message():
    customer=request.form['customer_identifier']
    message=request.form["message"]
    #we make sure the customer has his own queue
    channel.queue_declare(customer)
    channel.exchange_declare(exchange=customer, exchange_type="direct")
    channel.basic_publish(exchange=customer, routing_key=customer, body=message)

    res={
            "status": "success",
            "motive": "",
            "request": "add_message",
            "result": "message added"
        }
    return json.dumps(res)





connection.close()






app.run(host='0.0.0.0', port=80, debug=True)
