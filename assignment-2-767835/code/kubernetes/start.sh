#!/bin/bash

kubectl create -f mongodb-deployment.yaml
kubectl create -f rabbitmq-deployment.yaml

kubectl create -f mysimbdp-coredms.yaml
kubectl create -f mysimbdp-data-broker.yaml
kubectl create -f mysimbdp-fetch-data-batch.yaml
kubectl create -f mysimbdp-stream-ingest-manager.yaml

