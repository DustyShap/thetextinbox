FROM python:3.6.5
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code

ENV FLASK_APP=application.py
