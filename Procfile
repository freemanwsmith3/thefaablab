release: python faab/manage.py migrate --noinput
web: gunicorn faab.wsgi --chdir faab --workers ${WEB_CONCURRENCY:-3} --threads ${WEB_THREADS:-4} --timeout 30 --access-logfile - --error-logfile -
