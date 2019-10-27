import os
import json

import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
import pika
import http.client
from threading import Thread

app=Flask(__name__)



connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-service', 30015))
channel=connection.channel()


@app.route("/set_data_ingestion_function", methods=["POST"])
def set_data_ingestion_function():
    res={
            "status": "success",
            "motive": "",
            "request": "set_data_ingestion_function",
            "result": ""
        }
    customer=request.form['customer_identifier']
    func=request.form['function']
    
    filename=customer+"_ingestion_function.py"
    with open("/files/"+filename, "w") as f:
        f.write(func)
        f.close()
        res["result"]="File created: "+filename
    return json.dumps(res)



@app.route("/execute_ingestion", methods=["POST"])
def execute_ingestion():
    customer=request.form['customer_identifier']
    #TODO: get the file, put the function as callback for rabbitmq, and activate the reading of the whole queue
    channel.queue_bind(exchange=customer, queue=customer)
    channel.basic_consume(queue=customer, auto_ack=True, on_message_callback=callback)
    Thread t1=Thread(target=consume)
    t1.start()
    res={
            "status": "success",
            "motive": "",
            "request": "execute_ingestion",
            "result": ""
        }
    return json.dumps(res)

def consume():

    channel.start_consuming()
    return


def callback(ch, methods, properties, body):
    customer=method.routing_key
    #we get the instance
    data=json.loads(body)
    #we execute the function of the customer on this data
    # TODO

    #we send it to coredms
    try:
        connection=http.client.HTTPConnection("coredms-service", 30002)
        data={
                "customer_identifier": customer,
                "data": json.dumps(data)
            }
        headers={"Content-type": "application/json"}
        connection.request('POST', "/add_one_data", json.dumps(data), headers)
        response=connection.getresponse()
        connection.close()
    except HttpError as err:
        res['status']="failure"
        res['motive']="HttpError: "+ str(err)
        return json.dumps(err)
    except Exception as err:
        res['status']="failure"
        res['motive']="Exception: "+str(err)
        return json.dumps(res)
    response=response.read().decode()
    res['result']=response['data']['result']
    return json.dumps(res)
    













app.run(host='0.0.0.0', port=80, debug=True)
