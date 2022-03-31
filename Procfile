release: python manage.py makemigrations account --no-input
release: python manage.py migrate account --no-input
web: gunicorn projectone.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate