#!/bin/bash

rm search/migrations/*
python manage.py makemigrations search
python manage.py migrate

DJANGO_SETTINGS_MODULE=core.settings python imports.py

