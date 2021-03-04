from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Transaction
from decimal import Decimal

User = get_user_model()

@shared_task(serializer='json')
def send_transaction(source_user, target_user, currency_type, transfer_amount):

    try:
        get_source_user = User.objects.get(email=source_user)
        get_target_user = User.objects.get(email=target_user)

        if currency_type.lower() == 'btc':
            
            #credit btc wallet of target account
            get_target_user.btc_wallet_balance += Decimal(transfer_amount)
            get_target_user.save(update_fields=['btc_wallet_balance'])

            #debit btc wallet of source account
            get_source_user.btc_wallet_balance -= Decimal(transfer_amount)
            get_source_user.save(update_fields=['btc_wallet_balance'])

        elif currency_type.lower() == 'eth':

            #credit eth wallet of target account
            get_target_user.eth_wallet_balance += Decimal(transfer_amount)
            get_target_user.save(update_fields=['eth_wallet_balance'])

            #debit eth wallet of source account
            get_source_user.eth_wallet_balance -= Decimal(transfer_amount)
            get_source_user.save(update_fields=['eth_wallet_balance'])
        
        message = "success"
    
    except:
        message = "failed"

    return message


# @shared_task(serializer='json')
# def update_transaction_status(transaction_status, transaction_ref):
#     get_transaction_status=Transaction.objects.get(transaction_ref=transaction_ref)

#     return "seen"