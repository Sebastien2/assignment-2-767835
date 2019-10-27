gcloud config set project my-project-hello-world-255117
gcloud config set compute/zone europe-north1-a

gcloud container clusters create cluster1 --zone europe-north1-a
gcloud container clusters get-credentials cluster1



