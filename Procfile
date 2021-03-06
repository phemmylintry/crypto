release: python manage.py migrate
web: gunicorn crypto_transaction.wsgi --log-file -
worker: celery worker --app=tasks.app