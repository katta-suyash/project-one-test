release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate