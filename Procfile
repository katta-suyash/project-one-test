web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py makemigrations
manage.py migrate