import os
import json
import pandas as pd
import datetime
import time



#TODO: choose the file from which we get the data by unciommenting the rignt pair of lines
#batch evaluation
#filename="../mysimbdp-batchingestmanager/log_results"
#timestamp="timestamp"

#stream evaluation
filename="../mysimbdp-streamingestmanager/log_results"
timestamp="datetime"


def get_logs_to_pandas(name):
    with open(name, "r") as f:
        content=f.read()
        f.close()
    data=json.loads(content)
    #print(data[0])
    #print(data[1])
    #print(type(data[0]))
    data=pd.DataFrame(data)
    return data


def get_average_time_for_ingestion(data):
    somme=0
    nb=0
    for i in range(len(data)):

        d=data.iloc[i]
        if(i>0):
            #print(d[timestamp])
            #print(datetime.datetime.strptime(d[timestamp], "%Y-%m-%d %H:%M:%S.%f"))
            diff=datetime.datetime.strptime(d[timestamp], "%Y-%m-%d %H:%M:%S.%f")-datetime.datetime.strptime(data.iloc[i-1][timestamp], "%Y-%m-%d %H:%M:%S.%f")
            #print(diff)
            #we chack that it is not too big
            microseconds=diff.microseconds
            if(diff.days==0 and diff.seconds==0):
                #less than a secod: w take into account
                somme+=microseconds

                print(i, somme)
                nb+=1
    return (somme, nb)




data=get_logs_to_pandas(filename)
(somme, nb)=(get_average_time_for_ingestion(data))

avg=somme/nb
print("Time for a request (microseconds): "+ str(avg))
