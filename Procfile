web: gunicorn --pythonpath faab.wsgi
web: gunicorn faablab.wsgi:application --log-file - 
release: python manage.py migrate