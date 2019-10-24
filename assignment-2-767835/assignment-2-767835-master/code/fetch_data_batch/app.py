import os
import pandas as pd
from flask import Flask, redirect_url, url_for, request, render_template
from pymongo import MongoClient
import json


app=Flask(__name_)
client=MongoClient("http://mongodb:27017")
consumers=client.consumers

#table consumers holds the identity of all the consumers

@app.route('/read_consumer', methods=["POST"])
def read_consumer():
    consumer_name=request.form['consumer_name']
    consumer=consumers.find({'name': consumer_name})
    consumer=consumer[0]
    

    return str(consumer.dumps(consumer))


app.run(hos='0.0.0.0', port=80, debug=True)


