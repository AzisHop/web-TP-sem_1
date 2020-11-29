rm -rf mydatabase
rm -rf main/migrations
python3 manage.py makemigrations main
python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('Bars', '', 'Bars')" | python3 manage.py shell

python3 manage.py runserver
