import os
import http.client
import json


IP_coredms="35.228.247.66"


def hello_world():
    try:
        connexion=http.client.HTTPConnection(IP_coredms, 30002)
        headers={"Content-type": "application/json"}
        data=json.dumps({
                            "customer_identifier": "alice"
                        })
        connexion.request('GET', "/hello_world", data, headers)
        response=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "Exception: "+str(err)
    return response.read()
    response=json.loads(response)
    response=response['data']
    return json.dumps(response)



def create_account(my_name):
    try:
        connexion=http.client.HTTPConnection(IP_coredms, 30002)
        headers={"Content-type": "application/json"}
        data=json.dumps({
                            "customer_identifier": my_name
                        })
        connexion.request('POST', "/add_customer", data, headers)
        response=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "Exception: "+str(err)
    return response.read()
    response=json.loads(response)
    response=response['data']
    return json.dumps(response)


def get_description_database():
    try:
        connexion=http.client.HTTPConnection(IP_coredms, 30002)
        headers={"Content-type": "application/json"}
        data=json.dumps({})
        connexion.request('POST', "/description_database", data, headers)
        response=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "Exception: "+str(err)
    return response.read()
    response=json.loads(response)
    response=response['data']
    return json.dumps(response)






def testing():
    try:
        connexion=http.client.HTTPConnection(IP_coredms, 30002)
        headers={"Content-type": "application/json"}
        data=json.dumps({
                            "blob": "archange"
                        })
        connexion.request('POST', "/testing", data, headers)
        response=connexion.getresponse()
        connexion.close()
    except Exception as err:
        return "Exception: "+str(err)
    #return response.read()
    response=json.loads(response.read().decode())
    #return response
    #response=response['data']
    res2=response["result"]
    res2=res2['request.json']
    #res2=json.loads(res2)
    return res2
    #return json.dumps(response)


#print(hello_world())


print(testing())

#print(create_account("alice"))

#and then we get the description of the database
#print(get_description_database())
