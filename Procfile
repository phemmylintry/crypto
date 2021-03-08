release: python manage.py migrate
web: gunicorn crypto_transaction.wsgi --log-file -
worker: python manage.py qcluster