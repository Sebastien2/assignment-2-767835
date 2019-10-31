
***Assignment 2: data ingestion in the platform***

**Part 1**

*Question 1*

We use YAML format to write the constraints (maximum size of a file, type of the data, and maximum number of files). The YAML file ca be found in code/mysimbdp-fetch-data-batch/constraints.yaml. The client requests the file at fetch-data-batch:30012/get_constraints (POST request).

*Question 2*

The access to the client directories should not be accesible to mysimbdp for security reasons. Therefore, the client executes on his side a program that fetches all the files in the correct directory and sends those to mysimbdp. Thsi program is in client-fetch-data/send_files.py. It performs a separate request for each file. Then the compoenent mysimbdp-fetch-data-batch will receive the file and add it in its storage space, after modifying the name so that it is associated to the customer.

The other possibility to store the files is to write them as binary into the database. The advantage is that the files are then accessible from any pod, but it is increasing the amount of work of mysimbod-coredms.

*Question 3*

Storing the customer's function and executing it is performed within mysimbdp-fetch-data-batch. The function is first stored as a file, then executed on the content of each file. The function can modify the content of each file, and ingest as many instances of data as desired.

*Question 4*

Two consumers are defined: Alice and Bob. This is present in code/partial-pieces/mysimbdp-batchingestmanager/app.py. The logs are written in the database. The program puts the prformance logs into the file code/partial-pieces/mysimbdp-batchingestmanager/log_results. Each log contains 2 attributes: timestamp and nature. Obtaining the time to perform one ingestion is obtained by looking at the time difference between 2 ingestion requests.

The performance is obtained on 24000 data ingestions. On average, one ingestion is performed in 38.7 ms. However, there is no record of errors since the ingestion was performed entirely within the cluster.

*Question 5*

The ingestion is performed one by one, not by blocks of data. This reduces the performance, but improves the behaviour against errors. There are only a few data that is not ingested, but never a whole block of data. Therefore, statistics on the data are more reliable.


**Part 2**

![alt text][logo]
[logo]: https://github.com/Sebastien2/assignment-2-767835/tree/master/assignment-2-767835/assignment-2-767835-master/reports/partial_model.png "Stream ingestion model"


*Question 1*

A message contains the name of the customer, and one instance of data. This way, one message can be entirely indentified all on its own. Putting a single unit of data in each message increases the amount of communication, but helps the customer create an adapted function to deal with each data separately.

*Question 2*

The code is in code/partial-pieces/mysimbdp-streamingestmanager/app.py. It uses rabbitmq on local machine as a message broker. It saves the function written by the customer into files, and uses them during the consumption of the mesages. In this code, onece the consumption starts it cannot be stopped. The function of the customer can be changed again, so it is not a problem. The function clientstreamingestapp takes as entry one instance of data, in json format, can read it, and returns an instance of data in JSON format which can be different from the entry. Afterwards, the instance of data returned by the client's function is inserted into the database. The client does not have direct access to coredms, for security purposes. In this program, the database is mongodb on localhost.

*Question 3*

We develop tests for 2 different customers: Alice and Bob. The obtention of the logs is in the program code/partial-pieces/mysimbdp-streamingestmanager/app.py. This results in a file called log_results in the same folder. Each log contains 2 attributes: datetime and nature.

The result is that each data is ingested on average in 114.5 ms. This was obtained on 1400 ingestions.

*Question 4*

clientstreamingestapp is called for each data instance, therefore for each call it will store its performance in the database. For each call it will check the performances written and determine whether or not to send the report.
The report format must be in JSON with the attributes:
-customer_identifier: to identify whose function is being evaluated
-total_ingestion_size: number of bytes ingested
-average_ingestion_time: time ebtween 2 successive requests
-number_of_messages: just to be founf in the database
-beginning_report: time at which this report started to take the ingestion
-end_report: time at which this report ended to take the ingestion
-name_table: name of the table if the statistics were performed on a single table of the client's database

We use 2 tables to create the mechanism of transmitting the report to mysimbdp-streamingestmanager: ingestion_stats and client_performance_reports tables. ingestion_stats contains isntances of:
-name of customer
-size of data in bytes
-time of the ingestion
-duration of the ingestion
-name of the table in which it was ingested
-valid (boolean to check the validity)

client_performance_reports contains reports as described above.

Every time clientstreamingest is performed, it checks the time of the last report by this customer. If it is old enough, it starts creating a noew report by reading ingestion_stats on the instances of this cutomer recent enough. Once the report is created, it saves it in the database and sends it to mysimbdp-streamingestmanager.

*Question 5*

Every time mysimbdp-streamingestmanager receives a report, it reads the performance. If too low:
-it executes a script that creates a new instance of mysimbdp-streamingestmanager, and stores its name new_instance_streamingestmanager
-it sends a POST request to new_instance_streamingestmanager with the name of the customer, and the list of the files not yet ingested.
-it stops taking care of that customer


Any new instance will only have a single of the previously onnected customers, but a LoadBalancer service in kubernetes will send the new customers to this new instance until its load is as heavy a s the other instances.



**Part 3**

*Question 1*

![alt text][logo]
[logo]: https://github.com/Sebastien2/assignment-2-767835/tree/master/assignment-2-767835/assignment-2-767835-master/reports/complete_model.png "Complete platform model, ports written for each service"

Each blue square is a service. Behinf each service lies a deployment. The deployment runs on a cluster. The red square is the client. The blue links show the communications between servicces within the cluster, the red links show the services the client can access.

All services communicate through POST requests in HTTP. The parameters are sent in json format.

coredms-service is the only service with direct access to the database MongoDB. This ensures a control over the operations performed on the databases. The client has direct acces to coredms only to create and modify his customer profile. However, a more secure implementation would create an intermediate service for this, so that the customer never has access to coredms-service.

The batch ingestion is performed by a single batch: indeed, the data files provided by the customer must be accessible both for download and for ingestion. Therefore, it is more efficient to gather all functions within one pod, so that we do not make copies of the files from one pod to another. The batchingestmanager has a kubernetes volume in which is stored all the data files of all the customers, but also the files containing the ingestion functions specific to each customers.

The stream ingestion uses RabbitMQ as a message broker. The client sends the data to the data-broker service, which transforms it into messages into RabbitMQ. Then the client provides an ingestion function through stream-ingest-manager service, and initiates the consumption of messages. The consumption never stops (runs in a specific thread). Stream-ingest-manager sends the resulting data to coredms-service.


*Question 2*

In batchingestmanager, the function receiving the files checks the size. Very big files cannot be sent over in HTTP requests. On the client side, the file is sliced into small pieces to a specific service very_big_files_management_service. very_big_files_management_service receives each piece of the file separately, and gives it to the message broker. Once all the pieces have been received, the messages start to be consumed in order to rebuild the file, and store it on memory.

*Question 3*

The customers may put private or sensitive information on the platform. The ingestion of the platform may imply decrypting the files and/or the data. The trust of the customer cannot be obtained if the platform has access to all the customer's data. In addition, the platform should protect itself against attacks by ensuring that the platform itself cannot read the customer's data. Therefore, no security flaw can be the responsability of the platform, and data leaks are the responsability of the customers.

*Question 4*

The palatform provides a service in which the customer can define indicators and their acceptable values. For each data ingested, the customer has th possibility to call this service during the execution of clientstreamingestapp/clientbatchingestapp to check that the indicators on this data are accpetable. This way, the customer can easily check the quality of the data and at the same time protect its confidentiality (the customer decides which indicators are sent to this service).

*Question 5*

Eahc file of data/data-broker message is associated an attribute: thee category of data. The category refers to a specific client_ingestion function. This way, for each data (file or message), the platform can call the right client's function.
