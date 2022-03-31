release: python manage.py syncdb
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: python manage.py syncdb
web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput