rm -rf accounts/migrations/
rm -rf posts/migrations/
rm -rf groups/migrations/
rm -rf join_requests/migrations/
python manage.py makemigrations
python manage.py migrate
