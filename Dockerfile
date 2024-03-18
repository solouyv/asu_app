FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y python3-dev

WORKDIR /code

COPY requirements.txt /code/

RUN pip install pip==23.2.1 && pip install --no-cache-dir -r requirements.txt

COPY . /code/

WORKDIR /code/

EXPOSE 8000
