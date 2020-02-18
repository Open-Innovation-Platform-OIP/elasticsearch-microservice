#!/bin/bash
# access_token = 5b5efa54-6113-48e2-9053-79ce9b3b04f4
docker login --username tejpochiraju --password 5b5efa54-6113-48e2-9053-79ce9b3b04f4
docker build -t socialalphaoip/elasticsearch-microservice:dev .
docker push socialalphaoip/elasticsearch-microservice:dev