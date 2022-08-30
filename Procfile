release: python3 manage.py migrate
web: daphne Restaurent.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A Restaurent worker --beat --scheduler django --loglevel=info


