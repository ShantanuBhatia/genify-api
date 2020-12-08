FROM tiangolo/meinheld-gunicorn-flask:python3.8

MAINTAINER Shantanu Bhatia "sb5455@nyu.edu"

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update -y && \
    apt-get install -y libprotobuf-dev protobuf-compiler cmake gcc

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app