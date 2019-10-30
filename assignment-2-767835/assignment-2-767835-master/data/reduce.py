import os
import json
import datetime




with open("data.csv", "r") as f:
    content=f.read()
    f.close()


lines=content.split("\n")
with open("data2.csv", "w") as f:
    for i in range(10000):
        f.write(lines[i])
        f.write("\n")
    f.close()


