python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
# use better passwords
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell
python manage.py add_hls_file