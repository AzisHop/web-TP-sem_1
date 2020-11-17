rm -rf mydatabase
rm -rf app/migrations
python3 manage.py makemigrations main
python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python3 manage.py shell
python3 manage.py filldb
python3 manage.py runserver
