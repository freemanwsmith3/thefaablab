
web: gunicorn faablab.wsgi:application --log-file - 
web: python faablab/manage.py runserver 0.0.0.0:$PORT --noreload
release: python faablab/manage.py migrate