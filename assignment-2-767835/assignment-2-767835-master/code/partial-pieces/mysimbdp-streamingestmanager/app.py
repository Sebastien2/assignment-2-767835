import os
import pika
import json
import subprocess
from pymongo import MongoClient



mongo_client=MongoClient("mongodb-partial-service", 30020)







def callback(ch, methods, properties, body):
    #we get the customer's name
    customer=method.routing_key
    message=body

    #we execute the function on this messsage
    subprocess.run(["python3", "./"+customer+"_function.py", message])

    #we put the message in the database

    data=message['data']
    ''''
    try:
        connexion=http.client.HTTPConnection('coredms-service', 30002)
        headers{"Content-type": "application/json"}
        data={"customer_identifier": customer, "data": data}
        connexion.request("POST", "/add_one_data", data, headers)
        response=connexion.getresponse()
    except Exception as err:
        print("Excption: "+str(err))
    ''' 
    table=mongo_client.customer.customer
    table.insert_one(data)






#one function to add a message to the queue of the customer
def add_message(message):
    connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-partial-service', 30021))
    channel=connection.channel()
    
    customer=message['customer_identifier']
    channel.queue_declare(customer)
    channel.exchange_declare(exchange=customer, exchange_type="direct")
    channel.basic_publish(exchange=customer, routing_key=customer, body=str(message))

    connection.close()



#one function to define the client streaminapp
def define_personal_function(function):
    # we put the string of the function into a file
    with open("./"+customer+"_function.py", "w") as f:
        f.write(function)
        f.close()




#one function to start the consumption of the messages
def start_consuming(customer):
    connection=pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-partial-service', 30021))
    channel=connection.channel()

    queue_name=customer
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=customer, queue=customer)
    channel.basic_consume(queue=customer, on_message_callback=callback, auto_ack=True)


    channel.start_consuming()



    connection.close()





'''
#one function to stop the consumption of the messages
def stop_consuming(customer):
    connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel=connection.channel()

    queue_name=customer
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=customer, queue=customer)
    channel.basic_consume(queue=customer, on_message_callback=callback, auto_ack=True)


    channel.stop_consuming()



    connection.close()
'''






