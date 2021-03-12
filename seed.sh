#!/bin/bash
rm -rf breathapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations breathapi
python manage.py migrate breathapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata journals
python manage.py loaddata times
python manage.py loaddata types
python manage.py loaddata logs