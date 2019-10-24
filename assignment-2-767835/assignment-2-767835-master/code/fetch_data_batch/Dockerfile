FROM python:alpine

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["python3", "app.py"]

