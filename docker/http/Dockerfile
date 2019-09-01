FROM python:3.6.2-alpine
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code

RUN apk update
RUN apk add gcc musl-dev

RUN pip install --upgrade pip \
  && pip install -r requirements.txt
