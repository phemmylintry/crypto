release: python manage.py migrate
web: gunicorn crypto_transaction.wsgi --log-file -
worker: celery worker --crypto_transaction=tasks.app