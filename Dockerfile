FROM python:3.9.9-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y nginx
RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN pip install -e .
