web: python faab/manage.py runserver 0.0.0.0:$PORT
web: gunicorn faab/faab.wsgi:application --log-file - 
release: python faab/manage.py migrate