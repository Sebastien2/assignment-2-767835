import os
import json
import pandas as pd
import datetime
import time




filename="../mysimbdp-batchingestmanager/log_results"
#filename="../mysimbdp-streaingestmanager/log_results"



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


get_logs_to_pandas(filename)
