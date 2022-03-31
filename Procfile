release: python manage.py migrate --no-input
release: python manage.py makemigrations --no-input

web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate