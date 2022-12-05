# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /server
COPY requirements.txt /server/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /server/