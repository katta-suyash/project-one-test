release: python manage.py migrate account
web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate