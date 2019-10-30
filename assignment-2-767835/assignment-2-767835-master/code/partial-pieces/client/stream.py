import os
import json
import http.client
import subprocess
import time


IP="35.228.134.179"

def add_message(customer, data):
    try:
        connexion=http.client.HTTPConnection(IP, 30023)
        headers={"Content-type": "application/json"}
        data={
                "customer_identifier": customer,
                "message": data
            }
        connexion.request("POST", "/add_message", json.dumps(data), headers)
        res=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "failure: "+str(err)
    return res.read().decode()


def define_personal_function(customer, function):
    try:
        connexion=http.client.HTTPConnection(IP, 30023)
        headers={"Content-type": "application/json"}
        data={
                "customer_identifier": customer,
                "function": function
            }
        connexion.request("POST", "/define_personal_function", json.dumps(data), headers)
        res=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "failure 2:" + str(err)
    return res.read().decode()


def start_consuming(customer):
    try:
        connexion=http.client.HTTPConnection(IP, 30023)
        headers={"Content-type": "application/json"}
        data={
                "customer_identifier": customer
            }
        connexion.request("POST", "/start_consuming", json.dumps(data), headers)
        #res=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "failure 3:" + str(err)
    return "consumption has begun"



def get_logs(customer):
    try:
        connexion=http.client.HTTPConnection(IP, 30023)
        headers={"Content-type": "application/json"}
        data={
                "customer_identifier": customer
            }
        connexion.request("POST", "/get_logs", json.dumps(data), headers)
        res=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "failure 3:" + str(err)
    res=res.read().decode()
    return res







for i in range(10):
    print(add_message("alice", {"personne": "moi", "raison": "je m'aime"}))



print(define_personal_function("alice", ""))




print(start_consuming("alice"))

time.sleep(10)

print(get_logs("alice"))

