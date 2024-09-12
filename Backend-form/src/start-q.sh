echo "starting qcluster"
pkill -f "python manage.py qcluster"
nohup python manage.py qcluster &
