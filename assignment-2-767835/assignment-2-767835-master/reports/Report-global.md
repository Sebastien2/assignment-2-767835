*** Global description of the platform ***

The platform relies on kubernetes to manage docker images. The images are accessible through kubernetes services. All communications between services are peformed with POST requests in HTTP.
The database is MongoDB, and message broker is RabbitMQ. The tests were performed on Google Cloud Paltform.

** Global model **

![alt text][logo]
[logo]: https://github.com/Sebastien2/assignment-2-767835/tree/master/assignment-2-767835/assignment-2-767835-master/reports/complete_model.png "Complete platform model, ports written for each service"

The access to the database is performed through coredms. It is the only service with access to the database. This ensures security properties.
The client accesses the coredms service only to manage its customer profile (create/modify). Ideally, these operations would be performed through an internediate service dedicated to th profiles' management.

Otherwise, the client can access:
- stream-ingest-manager: to save his streamingestapp function as a file, and start consuming the messages from the databroker.
- data-broker: to add messages containing data.
- batch-ingest-manager: this service receives the data files, stores those; it also receives the batchingestapp function and stores it into a file; it also performs the ingestion by executing batchingestapp on the data files.

Files are stores with Kubernetes volumes, so that all instances can access the same folders.

In order to ensure availabilty, at least 3 instances of each image must run. In the code, the replicas are set to one for mere economy on GCP.

** Customer's profile **

Customer's profile are stored in MongoDB: the customers.customers colloection contains all the profiles. A profile is a name (unique), and the name of the associated database. No security element was included (password, salt, ...). The profiles are minimal.


** Customer's data **

Each customer wants a personal space to manage its data. Therefore, each customer is attributed one different database. In the database, the client can create as many collections as desired, and send each data to a specific collection. In the implementation, only one table is used for each customer.

** Customer's functions **

The ingestion functions take as argument the name of the customer, a name associated to the data (name of the file or type of the message), and the data itself. The client's function reads the data as a string, and calls a function from the API to ingest instances of data. This ingestion function can be called as many times as intended.


** Testing the ingestion **

The testing was performed with light clientstreamingestapp/clientbatchingestapp functions. We obtained:
-batch ingestion: on 24000 ingestions, 38.7 ms per ingestion
-stream ingestion: on 1400 ingestions, 114.4 ms per ingestion

The batch ingestion is faster than the stream ingestion.

** Logging features **

In order to have a feedback on the ingestion, a new database is used, called logs. It stores for each ingestion:
- the timestamp of the ingestion
- the customer associated to this ingestion
- the result of the ingestion (success/failure, with the reason)
- the name of the table in which it was stored
- the byte size of the data

Each ingestion also add the corresponding log. This way, it is possible to notice failure peaks with their cause (a specific customer, an activity peak, the type/size of the data, ...). The logs datablase are accessible to the platform for analytics, and also to the customers (each customer his own logs). If the customer requests his logs, they are send in JSON format in a file.

*** Implementation ***

Different programs work separately.

** Batch ingestion **

The batch ingestion was implemented locally. It requires a running instance of MongoDB on the local machine.
python3 code/partial-pieces/mysimbdp-batchingestmanager/app.py

In this program, the customer profile can be modified at the end of the program. The program can be run in GCP with MongoDB running on cluster: the IP addresses and ports of the 2 servies must be changed accordingly, and it is all.

The program returns the logs in the file code/partial-pieces/mysimbdp-batchingestmanager/log_results (which already exists).

** Stream ingestion **

The stream ingestion was implemented on GCP, with MongoDB and RabbitMQ running as services on a cluster. It can also be run locally by changing the ports and IPs of both services accordingly.
There are 2 profiles defined: Alice and Bob.

** Global model implementation **

The main implementation aimed at a whole platform on Kubernetes with all the services described in the top schema. This implementation is not fully working however due to lack of time. The services can be deployed on Google Cloud Paltform, they are running and communicationg with one another correctly (hello_world requests have been successful). However, all the useful requests are not working: many errors are left, and prevent any use of the services. This implementation uses the following folders:
- code/kubernetes (except code/kubernetes/partial-pieces): contains the configuration files for all the services. The replicas are set to 1 for testing. For deployment, they should be set to at least 3.
- code/mysimbdp-batch-ingest-manager: contains the files to create the Docker image for this service
- code/mysimbdp-coredms: contains the files to create the Docker image for this service
- code/mysimbdp-data-broker: contains the files to create the Docker image for this service
- code/mysimbdp-stream-ingest-manager: contains the files to create the Docker image for this service

In order to run the services:
- ./code/gcloud_config.sh : creates a cluster on GCP, and configures it as the default cluster
- ./code/docker_building.sh: creates all the docker images, and stores them on gcr.io
- ./code/kubernetes/start.sh: starts all deployments and services
- ./code/kubernetes/end.sh: stops all deployments and services. Warning: the cluster must be removed afterwards.

A hello_world request can be performed with curl: curl [external_IP of coredms-service]/hello_world. Sadly, most other requests do not work.
