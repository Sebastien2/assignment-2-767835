#!/bin/bash

kubectl apply -f mongodb-deployment.yaml
kubectl apply -f rabbitmq-deployment.yaml

kubectl apply -f mysimbdp-coredms.yaml
kubectl apply -f mysimbdp-data-broker.yaml
kubectl apply -f mysimbdp-fetch-data-batch.yaml
kubectl apply -f mysimbdp-stream-ingest-manager.yaml

