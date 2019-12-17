FROM python:3.7-alpine

COPY . /analyzer
WORKDIR /analyzer

RUN pip install -r requirements.txt

