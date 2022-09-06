web: python faab/manage.py runserver 0.0.0.0:$PORT
web: gunicorn faablab.wsgi:application --log-file - 
release: python faab/manage.py migrate