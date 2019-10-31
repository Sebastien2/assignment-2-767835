import os
import json
import http.client
import requests


IP_fetch_data_batch=""


def scavenge_direcory(path):
    for entry in os.scandir(path):
        if(entry.is_dir()):
            if("client-input-directory" in entry.path):
                #we return this path
                return entry.path
            else:
                return scavenge_directory(entry.path)


def get_files_names():
    folder=scavenge_directory('/')
    files=[]
    if (folder is None):
        return "Error: folder client-input-file inexistent"
    else:
        #we make the lists of all files in the folder
        for entry in os.scandir(folder):
            if(entry.is_file()):
                files.append(entry.path)
    return files



def send_files(files):
    #for each file, we send a request to add it
    url=IP_fetch_data_batch+":30012/add_file"
    for f in files:
        fls={'file': open(f, 'rb')}
        r=requests.post(url files=fls)



files=get_files_names()
if "Error: " in files:
    print files
else:
    send_files(files)
    return "files sent"


