# Use an official Python runtime as a parent image
FROM amancevice/pandas:0.25.0

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python3", "app.py"]
