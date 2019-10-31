import subprocess
import os
import json
from pymongo import MongoClient
import pandas as pd
import datetime
import time

IP_mongo="localhost"

mongo_client=MongoClient(IP_mongo)
#NOTE For execution on GCP, uncomment
#mongo_client=MongoClient(IP_on_the_clsuter, port_on_the_cluster)



def save_file(customer, path):
    with open(path, 'r') as source:
        content=source.read()
        source.close()
    with open("./"+customer+"_data_"+os.path.basename(path), "w") as f:
        f.write(content)
        f.close()


    return "file "+path +" saved"







def save_personal_function(customer, function):
    with open("./"+customer+"_function", "w") as f:
        f.write(function)
        f.close()



def ingest_files(customer):
    #print("ingest_files started")
    #we get the list of the file names
    files=get_data_files(customer)
    #we get tje name of the ingestion function
    ingestion_function_name=get_ingestion_file(customer)
    #for each file, we read and ingest
    for filename in files:
        data=pd.read_csv(filename)
        #conversion to json

        #print(data)
        #print(type(data))
        execute_one_file(customer, ingestion_function_name, data)


def execute_one_file(customer, ingestion_function, data):
    #print("execute_one_file started")
    #we first modify if necessary the columns names
    columns=data.columns.values
    #print(columns)
    for index, col in enumerate(columns):
        col=col.replace('.', '_')
        columns[index]=col
    data.columns=columns
    print("number of data: "+ str(len(data.index)))
    for index, row in data.iterrows():
        if(index%1000==0):
            print("index: "+str(index) + " "+ str(type(row)))
        line=row.to_json()
        line=json.loads(line)
        #print(line)
        #print(type(line))
        #we execute the user's function
        subprocess.run(["python3", "./"+customer+"_function", json.dumps(line)])
        #we insert in the database
        mongo_client[customer][customer].insert_one(line)
        # and the logs
        mongo_client['logs'][customer].insert_one({"timestamp": str(datetime.datetime.now()), "nature": "insert one data batch"})
        #print(type(row))

    return



def get_data_files(customer):
    res=[]
    for f in os.listdir("./"):
        if(os.path.isfile(f)):
            if(customer+"_data_" in f):
                res.append(f)
    return res


def get_ingestion_file(customer):
    name="./"+customer+"_function"
    return name




def get_logs(customer):
    table=mongo_client.logs[customer]
    res=[elem for elem in table.find({},{"_id": 0})]
    #return str(len(res))
    return json.dumps(res)



#testing: NOTE: choose the user
customer="bob"

#we put a file
if(customer=="alice"):

    print("saving the file...")
    save_file("alice", "./../../../data/data2.csv")

    print("saving the ingestion function ...")
    save_personal_function("alice", "print('and one ingestion')")

    print("ingesting the files...")
    ingest_files("alice")

    print("getting the logs...")
    logs=get_logs("alice")
    with open("./log_results", "w") as f:
        f.write(logs)
        f.close()


    print("done")
elif(customer=="bob"):
    print("saving the file...")
    save_file("bob", "./../../../data/data2.csv")

    print("saving the ingestion function ...")
    save_personal_function("bob", "")

    print("ingesting the files...")
    ingest_files("bob")

    print("getting the logs...")
    logs=get_logs("bob")
    with open("./log_results", "w") as f:
        f.write(logs)
        f.close()


    print("done")
