rm -rf accounts/migrations/
rm -rf posts/migrations/
rm -rf groups/migrations/
python manage.py makemigrations
python manage.py migrate
