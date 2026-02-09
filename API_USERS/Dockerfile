FROM python:3.13

WORKDIR /code

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*
 
COPY ./dependances.txt /code/dependances.txt

RUN pip install --no-cache-dir --upgrade -r /code/dependances.txt

COPY app /code/app
