import os
import json

import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app=Flask(__name__)

#client=MongoClient("mongodb://database:27017/")
client_mongo=MongoClient('mongodb://mongodb-service', 30001)

#to rewrite: mainly useless functions 
db=client.db_1

#print
@app.route('/show_html')
def show_html():
    _items=db.table_1.find()
    items=[item for item in _items]
    return render_template('todo.html', items=items)


@app.route('/show_length_database')
def show_length_database():
    _items=db.table_1.find()
    items=[item for item in _items]
    #return render_template('show_length_database.html', len=len(items))
    return str(len(items))

#test
@app.route('/hello_world')
def hello_world():
    return "hello world"


#put
@app.route('/insert_one', methods=['POST'])
def insert_one():
    #on récupère les arguments
    table=db.table_1

    table.insert_one()

    return "done"


@app.route('/insert_many', methods=["POST"])
def insert_many():
    table=db.table_1
    #on récupère le json en POST
    json=request.form['data']
    #on l'inser dasn la bdd
    data=pd.read_json(json)

    res=table.insert_many(data.to_dict('records'))
    #on revoie un resultat

    return str(res.inserted_ids)



@app.route('/delete_all')
def delete_all():
    table=db.table_1
    result=table.delete_many({})
    return "Number of deleted instances: "+str(result.deleted_count)














#useful functions
@app.route('/get_customer', method=["POST"])
def get_customer():
    #get the arg, which is the name of the customer
    customer_name=request.form['customer_name']
    table=client_mongo.customers
    customer=table.find_one({"name": customer_name})
    return json.dumps(customer)


#should not be useful, except for debugging
@app.route('get_all_customers', method=["POST"])
def get_all_customers():
    table=client_mongo.customers
    customers=table.find()
    return json.dumps(customers)


@app.route("/add_customer", method=["POST"])
def add_customer():
    customer_identifier=request.form['customer'] #just contains the identifier of the customer -> it must not already exist (like an email for instance)
    table=client_mongo.customers
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
        result=db.customers.insert_one({
                                        "identifier": customer_identifier,
                                        "name_table": "table"+customer_identifier
                                     })
        res={
                "status": "success",
                "motive": "",
                "request": "add_customer",
                "result": result
             }
    return json.dumps(res)


#get the data functions
@app.route('/get_all_data', method=["POST"])
def get_all_data():
    #we get the naem of the customer
    customer=request.form['customer']
    customer=db.customers.find_one({"identifier": customer})
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
        res={
                "status": "success",
                "motive": "",
                "request": "get_all_data",
                "result": json.dumps(data)
             }
    return json.dumps(res)


@app.route("/get_one_data", method=["POST"])
def get_one_data():     
    #we get the naem of the customer
    customer=request.form['customer']
    customer=db.customers.find_one({"identifier": customer})
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
        table=db[table_name]
        data=table.find_one({"_id": data_id})
        res={
                "status": "success",
                "motive": "",
                "request": "get_all_data",
                "result": json.dumps(data)
             }
    return json.dumps(res)


#add data
@app.route("/add_one_data", method=["POST"])
def add_one_data():
    data=request.form['data']
    data=pd.read_json(data)
    data=data.to_dict('records')
    #we check the customer

    customer=request.form['customer']
    customer=db.customers.find_one({"identifier": customer})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "add_one_data",
                "result": ""
            }
    else:
        table=db[customer['name_table']]
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
@app.route("/add_many_data", method=["POST"])
def add_many_data():
    data=request.form['data']
    data=pd.read_json(data)
    data=data.to_dict('records')
    #we check the customer

    customer=request.form['customer']
    customer=db.customers.find_one({"identifier": customer})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "add_many_data",
                "result": ""
            }
    else:
        table=db[customer['name_table']]
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
@app.route("/get_length_table", method=["POST"])
def get_length_table():
    #we check the customer
    customer=request.form['customer']
    customer=db.customers.find_one({"identifier": customer})
    if(customer is None):
        res={
                "status": "failure",
                "motive": "customer does not exist",
                "request": "get_length_table",
                "result": ""
            }
    else:
        table=db[customer['name_table']]
        l=len([item for item in table.find()]
        res={
                "status": "success",
                "motive": "",
                "request": "get_length_table",
                "result": l
            }

    return json.dumps(res)





app.run(host='0.0.0.0', port=80, debug=True)
