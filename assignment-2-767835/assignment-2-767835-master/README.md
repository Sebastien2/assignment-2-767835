# Assignment Assignment_2  767835

* Reports *

There are 2 reports in /reports/ : one follows the questions, the other one follows how I worked on the project. The second one contains more information on  implementation.

* data *

This folder contains a sample of csv data from water quality in UK database. It has been used on the example customers.

* code *

This folder contains the code for several deployments.
In /kubenetes, there are the configuration files for deployments and services
In the folders /code/mysimbdp-\*, there are the programs that are used to create Docker images. The Docker images are then called in the kubernetes configuration files.
In the folder /code/partial-pieces, there are programs implementing pieces of the data platform design. Within, there are:
- mysimbdp-batch-ingest-manager: app.py is the program to be executed.
- mysimbdp-stream-ingest-manager: app.py is the program to be executed
- client: useless
- log_analysis: contains a program to get the performance of log files

* Global description *

My first goal was to implement the whole platform (Question 3.1) directly, which would also help me learn to use Kubernetes and Google Cloud. This implementation turned out to take too much time: there are still errors in it. partial-pieces folders therefore implement isolated ingestion features of the platform. They are correct programs.
The description of the scripts to use can be found in one of the reports. 
