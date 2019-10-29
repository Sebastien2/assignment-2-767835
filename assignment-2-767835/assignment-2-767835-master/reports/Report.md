
***Assignment 2: data ingestion in the platform***

**Part 1**

*Question 1*

We use YAML format to write the constraints (maximum size of a file, type of the data, and maximum number of files). The YAML file ca be found in code/mysimbdp-fetch-data-batch/constraints.yaml. The client requests the file at fetch-data-batch:30012/get_constraints (POST request).

*Question 2*

The access to the client directories should not be accesible to mysimbdp for security reasons. Therefore, the client executes on his side a program that fetches all the files in the correct directory and sends those to mysimbdp. Thsi program is in client-fetch-data/send_files.py. It performs a separate request for each file. Then the compoenent mysimbdp-fetch-data-batch will receive the file and add it in its storage space, after modifying the name so that it is associated to the customer.

The other possibility to store the files is to write them as binary into the database. The advantage is that the files are then accessible from any pod, but it is increasing the amount of work of mysimbod-coredms.

*Question 3*

Storing the customer's function and executing it is performed within mysimbdp-fetch-data-batch. The function is first stored as a file, then executed on the content of each file. The function can modify the content of each file. Then, the new content is written into the database.

*Question 4*


*Question 5*

The ingestion is performed by blocks of data (not one by one). For each block, we write into the log the number of data instances, the date of beginning of ingestion, and the date of end of ingestion, so that we can determine the rythm of ingestion. We also add the number of successful storing, and the number of failures. This can be saved into the database (separate collection).


**Part 2**

*Question 1*

A message contains the name of the customer, and one instance of data. This way, one message can be entirely indentified all on its own. Putting a single unit of data in each message increases the amount of communication, but helps the customer create an adapted function to deal with each data separately.

*Question 2*

The code is in code/partial-pieces/mysimbdp-streamingestmanager/app.py. It uses rabbitmq on local machine as a message broker. It saves the function written by the customer into files, and uses them during the consumption of the mesages. In this code, onece the consumption starts it cannot be stopped. The function of the customer can be changed again, so it is not a problem. The function clientstreamingestapp takes as entry one instance of data, in json format, can read it but not modify it. It does nto return anything. Afterwards, the instance of data is inserted into the database. In this program, the database is mongodb on localhost.

*Question 3*



*Question 4*


