import os
import json

import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient


app=Flask(__name__)

#client=MongoClient("mongodb://database:27017/")
client_mongo=MongoClient('mongodb://mongodb-service', 30001)



@app.route('/show_length_database', methods=['POST', 'GET'])
def show_length_database():
    _items=client_mongo.customers.find({},{"_id": 0} )
    items=[item for item in _items]
    #return render_template('show_length_database.html', len=len(items))
    return str(len(items))

#test
@app.route('/hello_world', methods=['POST', 'GET'])
def hello_world():
    return "hello world"

@app.route("/description_database", methods=["POST"])
def description_database():
    # we give for each collection, the list of tables with the size of the table
    dbs=client_mongo.list_database_names()
    res={
            "status": "success",
            "motive": "",
            "request": "/description_database",
            "result": ""
        }
    contenu=""
    for database in dbs:
        db=client_mongo.database
        contenu+=database+"\n"
        tables=db.list_collections_names()
        for table in tables:
            tb=db.table
            size=len(tb.find({}))
            contenu+="    "+table+": "+str(size)+"\n"
    res['result']=contenu
    return json.dumps(res)









#useful functions
@app.route('/get_customer', methods=["POST"])
def get_customer():
    #get the arg, which is the name of the customer
    customer_name=request.form['customer_identifier']
    table=client_mongo.customers.customers
    customer=table.find_one({"identifier": customer_name})
    return json.dumps(customer)

    
#should not be useful, except for debugging
@app.route('/get_all_customers', methods=["POST"])
def get_all_customers():
    table=client_mongo.customers.customers
    customers=table.find({}, {"_id": 0})
    customers=[item for item in customers]
    return json.dumps(customers)


@app.route("/add_customer", methods=["POST"])
def add_customer():
    customer_identifier=request.form['customer_identifier'] #just contains the identifier of the customer -> it must not already exist (like an email for instance)
    table=client_mongo.customers.customers
    name_table=customer_identifier
    customer={
            "identifier": customer_identifier,
            "name_table": name_table
            }
    previous_customers=table.find({"identifier": customer_identifier})
    previous_customers=[previous for previous in previous_customers]
    if(len(previous_customers)>0):
        res={
                "status": "failure",
                "motive": "identifier already exists",
                "request": "add_customer",
                "result": 0
            }
    else:
        #we insert the customer as requested
        result=customers.insert_one({
                                        "identifier": customer_identifier,
                                        "name_table": name_table
                                     })
        res={
                "status": "success",
                "motive": "",
                "request": "add_customer",
                "result": result
             }
    return json.dumps(res)




@app.route('/testing', methods=["POST"])
def testing():
        res={
                "status": "success",
                "motive": "",
                "request": "testing",
                "result": 0
            }
        content={}
        content["request.form"]=(request.form)
        content["request.args"]=(request.args)
        content["request.values"]=(request.values)
        content["request.json"]=(request.json)
        res["result"]=(content)
        return json.dumps(res)



#get the data functions
@app.route('/get_all_data', methods=["POST"])
def get_all_data():
    #we get the naem of the customer
    customer=request.form['customer']
    customer=client_mongo.customers.customers.find_one({"identifier": customer}, {"_id": 0})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "get_all_data",
                "result": ""
            }
    else:
        table_name=customer['name_table']
        table=db[table_name]
        data=table.find()
        data=[elem for elem in data]
        res={
                "status": "success",
                "motive": "",
                "request": "get_all_data",
                "result": json.dumps(data)
             }
    return json.dumps(res)


@app.route("/get_one_data", methods=["POST"])
def get_one_data():     
    #we get the naem of the customer
    customer_id=request.form['customer']
    customer=client_mongo.customers.customers.find_one({"identifier": customer_id}, {"_id": 0})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "get_one_data",
                "result": ""
            }
    else:
        data_id=request.form["data_id"]
        table_name=customer['name_table']
        table=client_mongo[customer_id][table_name]
        data=table.find_one({"_id": data_id})
        res={
                "status": "success",
                "motive": "",
                "request": "get_all_data",
                "result": json.dumps(data)
             }
    return json.dumps(res)


#add data
@app.route("/add_one_data", methods=["POST"])
def add_one_data():
    data=request.form['data']
    data=pd.read_json(data)
    data=data.to_dict('records')
    #we check the customer

    customer=request.form['customer']
    customer=client_mongo.customers.customers.find_one({"identifier": customer})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "add_one_data",
                "result": ""
            }
    else:
        table=db[customer['identifier']][customer['name_table']]
        result=table.insert_many(data)
        result=[item for item in result.inserted_ids]
        res={
                "status": "success",
                "motive": "",
                "request": "add_one_data",
                "result": json.dumps(result)
            }
    return json.dumps(res)


#we create the same function for adding many elements -> check if both works TODO
@app.route("/add_many_data", methods=["POST"])
def add_many_data():
    data=request.form['data']
    data=pd.read_json(data)
    data=data.to_dict('records')
    #we check the customer

    customer=request.form['customer']
    customer=client_mongo.customers.customers.find_one({"identifier": customer})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "add_many_data",
                "result": ""
            }
    else:
        table=db[customer["identifier"]][customer['name_table']]
        result=table.insert_many(data)
        result=[item for item in result.inserted_ids]
        res={
                "status": "success",
                "motive": "",
                "request": "add_many_data",
                "result": json.dumps(result)
            }
    return json.dumps(res)


#find length of the table
@app.route("/get_length_table", methods=["POST"])
def get_length_table():
    #we check the customer
    customer=request.form['customer_identifier']
    customer=client_mongo.customers.customers.find_one({"identifier": customer})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "get_length_table",
                "result": ""
            }
    else:
        table=client_mongo[customer["identifier"]][customer['name_table']]
        l=len([item for item in table.find()])
        res={
                "status": "success",
                "motive": "",
                "request": "get_length_table",
                "result": l
            }

    return json.dumps(res)



@app.route("/get_file", methods=["POST"])
def get_file():
    #on trouve le fichier de cette personne avec ce fileneme, et on le renvoie en texte
    customer=request.form['customer_identifier']
    filename=request.form['filename']

    complete_name=customer+"_"+filename
    table=client_mongo.files.files
    entity=table.find_one({'filename': complete_name}, {"_id": 0})
    res={
            "status": "success",
            "motive": "",
            "request": "get_file",
            "result": entity
        }
    return json.dump(res)


#to add a file
@app.route("/add_file", methods=["POST"])
def add_file():
    customer=request.form['customer_identifier']
    filename=request.form['filename']
    content=request.form['file']

    #and we put it in the database
    table=client_mongo.files.files
    result=table.insert_one({
                                "customer": customer,
                                "filename": filename,
                                "file": content,
                                "ingested": 0
                            })
    res={
            "status": "success",
            "motive": "",
            "request": "add_file",
            "result": ""
        }
    return json.dumps(res)


@app.route("/get_all_my_files", methods=["POST"])
def get_all_my_files():
    res={
            "status": "success",
            "motive": "",
            "request": "get_all_my_files",
            "result": ""
        }

    
    customer=request.form['customer_identifier']

    table=client_mongo.files.files

    #we get all the files of this customer
    rows=table.find({"customer": customer}, {"_id": 0})
    rows=[item for item in rows]
    res['result']=rows
    return json.dumps(res)












app.run(host='0.0.0.0', port=80, debug=True)
