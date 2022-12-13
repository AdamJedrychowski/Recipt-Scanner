#!/bin/bash

docker compose exec server python3 /server/manage.py makemigrations

docker compose exec server python3 /server/manage.py migrate