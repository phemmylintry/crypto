release: python manage.py migrate
web: gunicorn crypto_transaction.wsgi --log-file -
worker: celery -A crypto_transaction.celery worker -B --loglevel=info