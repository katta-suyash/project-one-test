
release: python manage.py migrate --run-syncdb --no-input
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate