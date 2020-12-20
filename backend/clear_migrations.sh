rm accounts/migrations/0*
rm posts/migrations/0*
rm groups/migrations/0*
python manage.py makemigrations
python manage.py migrate
