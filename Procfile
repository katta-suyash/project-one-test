release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: python manage.py runserver --no-input

web: gunicorn projectone.wsgi --log-file