FROM python:3.7

RUN mkdir /app
WORKDIR /app

ENV DATABASE_URL postgres://postgres@localhost/postgres

ADD requirements.txt /app/
ADD requirements_test.txt /app/

RUN pip install -U pip
RUN pip install -r /app/requirements_test.txt

RUN apt update && apt install -y mc mysql-client

ADD src /app/

EXPOSE 8000
