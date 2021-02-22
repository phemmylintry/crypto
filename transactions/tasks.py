from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_transaction(currency_type, currency_amount, target_user, source_user):
    target_user = 

    return "Hello world"