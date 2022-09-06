
web: gunicorn faablab.wsgi:application --log-file - 
--pythonpath django_structure/src faab.wsgi

release: python faablab/manage.py migrate