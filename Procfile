
web: gunicorn faablab.wsgi:application --log-file - 
--pythonpath django_structure/src django_structure.wsgi

release: python manage.py migrate