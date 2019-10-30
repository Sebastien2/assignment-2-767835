import subprocess
import os
import json
import pymongo



def save_file(customer, path):
    with open(path, 'r")') as source:
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
    #we get the list of the file names
    files=get_data_files(customer)
    #we get tje name of the ingestion function
    ingestion_function_name=get_ingestion_file(customer)
    #for each file, we read and ingest
    for filename in files:
        with open(filename, "r") as f:
            data=f.read()
            f.close()
        print(data)
        print(type(data))



def get_data_files(customer):
    res=[]
    for f in os.listdir("./"):
        if(isfile(f)):
            if(customer+"_data_" in f):
                res.append(f)
    return res


def get_ingestion_file(customer):
    name="./"+customer+"_function"
    return name






#testin



