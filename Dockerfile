FROM python:3.7

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
ADD requirements_test.txt /app/

RUN pip install -U pip
RUN pip install -r /app/requirements_test.txt

ADD src /app/

EXPOSE 8000
