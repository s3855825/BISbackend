release: python backend/manage.py makemigrations accounts posts groups && python backend/manage.py migrate --no-input
web: gunicorn --pythonpath backend backend.wsgi --log-file -