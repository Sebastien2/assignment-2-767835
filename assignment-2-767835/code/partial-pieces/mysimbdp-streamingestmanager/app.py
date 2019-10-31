import os
import pika
import json
import subprocess
from pymongo import MongoClient
from flask import Flask, request
import datetime
import time
import threading
import sys

#TODO: modify the IPs
IP_mongo="35.228.109.116"
IP_rabbit="35.228.247.66"

mongo_client=MongoClient(IP_mongo, 30020)



app=Flask(__name__)







def callback(ch, methods, properties, body):
    #we get the customer's name
    customer=methods.routing_key
    message=(body.decode())
    message=message.replace("'", "\"")
    #we execute the function on this messsage
    subprocess.run(["python3", "./"+customer+"_function.py", message])

    #we put the message in the database
    data=message
    data=json.loads(data)
    #print(data)
    #print(data.keys())
    table=mongo_client.customer.customer

    table.insert_one(data)

    #second insertion: for the logs
    logs_table=mongo_client.logs[customer]
    logs_table.insert_one({"datetime": str(datetime.datetime.now()), "nature": "insertion one data stream"})
    #print("callback performed")










#one function to add a message to the queue of the customer
def add_message(message):
    connection=pika.BlockingConnection(pika.ConnectionParameters(IP_rabbit, 30021))
    channel=connection.channel()

    customer=message['customer_identifier']
    channel.queue_declare(customer)
    channel.exchange_declare(exchange=customer, exchange_type="direct")
    channel.basic_publish(exchange=customer, routing_key=customer, body=str(message))

    connection.close()



#one function to define the client streaminapp
def define_personal_function(customer, function):
    # we put the string of the function into a file
    with open("./"+customer+"_function.py", "w") as f:
        f.write(function)
        f.close()




#one function to start the consumption of the messages
def start_consuming(customer):
    connection=pika.BlockingConnection(pika.ConnectionParameters(IP_rabbit, 30021))
    channel=connection.channel()

    queue_name=customer
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=customer, queue=customer)
    channel.basic_consume(queue=customer, on_message_callback=callback, auto_ack=True)


    channel.start_consuming()



    connection.close()



def get_logs(customer):
    table=mongo_client.logs[customer]
    res=[elem for elem in table.find({},{"_id": 0})]
    #return str(len(res))
    return json.dumps(res)



@app.route("/add_message", methods=["POST"])
def add_message_route():
    customer=request.json['customer_identifier']
    content=request.json['message']
    add_message({"customer_identifier": customer , "data": content})
    return "done successfully"

@app.route("/define_personal_function", methods=["POST"])
def define_personal_function_route():
    function=request.json['function']
    customer=request.json['customer_identifier']
    define_personal_function(customer, function)
    return "done successfully 2"

@app.route("/start_consuming", methods=["POST"])
def start_consuming_route():
    customer=request.json['customer_identifier']
    start_consuming(customer)
    return "done successfully 3"



@app.route("/get_logs", methods=["POST"])
def get_logs_route():
    customer=request.json["customer_identifier"]
    return get_logs(customer)


#app.run(host='0.0.0.0', port=80, debug=True)



def consume():
    start_consuming("alice")


#TODO: choose the customer
customer="alice"


if(customer=="alice"):
    for i in range(1000):
        add_message({"customer_identifier": "alice", "data": "bob morane l aventurier est passe par la"})
        print("message aadding: "+ str(i) + "/1000")
    define_personal_function("alice", "")
    #define_personal_function"alice", "print('Ingestion of one data')")

    t=threading.Thread(target=consume)
    t.start()
    print("consumption begun")

    time.sleep(200)

    logs=get_logs("alice")
    with open("./og_results", "w") as f:
        f.write(logs)
        f.close()

    print("logs written")
elif(customer=="bob"):
        for i in range(1000):
            add_message({"customer_identifier": "bob", "data": "jack the reaper was in london"})
            print("message aadding: "+ str(i) + "/1000")
        define_personal_function("bob", "print('ses fluctuat nec mergitur')")
        #define_personal_function"alice", "print('Ingestion of one data')")

        t=threading.Thread(target=consume)
        t.start()
        print("consumption begun")

        time.sleep(200)

        logs=get_logs("bob")
        with open("./log_results", "w") as f:
            f.write(logs)
            f.close()

        print("logs written")
