release: python3 manage.py migrate
web: bin/start-pgbouncer-stunnel gunicorn Restaurent.wsgi
main_worker: python3 manage.py celery worker --beat --loglevel=info


