import os
import json
import datetime

#This script is to reduce the amout of data in a file: it is not to be used
#NOTE DO NOT USE


with open("data.csv", "r") as f:
    content=f.read()
    f.close()


lines=content.split("\n")
with open("data2.csv", "w") as f:
    for i in range(10000):
        f.write(lines[i])
        f.write("\n")
    f.close()
