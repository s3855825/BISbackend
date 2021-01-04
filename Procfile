release: python backend/manage.py makemigrations accounts posts groups && python manage.py migrate --no-input
web: gunicorn --pythonpath backend backend.wsgi --log-file -