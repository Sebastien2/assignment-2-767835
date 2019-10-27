
VERSION="v0.6"

docker build ./mysimbdp-coredms/ -t gcr.io/my-project-hello-world-255117/mysimbdp-coredms:$VERSION
docker build ./mysimbdp-data-broker/ -t gcr.io/my-project-hello-world-255117/mysimbdp-data-broker:$VERSION
docker build ./mysimbdp-fetch-data-batch/ -t gcr.io/my-project-hello-world-255117/mysimbdp-fetch-data-batch:$VERSION
docker build ./mysimbdp-stream-ingest-manager/ -t gcr.io/my-project-hello-world-255117/mysimbdp-stream-ingest-manager:$VERSION

docker push gcr.io/my-project-hello-world-255117/mysimbdp-coredms:$VERSION
docker push gcr.io/my-project-hello-world-255117/mysimbdp-data-broker:$VERSION
docker push gcr.io/my-project-hello-world-255117/mysimbdp-fetch-data-batch:$VERSION
docker push gcr.io/my-project-hello-world-255117/mysimbdp-stream-ingest-manager:$VERSION






