web: gunicorn --pythonpath faab/faab.wsgi
web: gunicorn faablab.wsgi:application --log-file - 
release: python manage.py migrate