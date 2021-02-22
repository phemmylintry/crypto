from django.db import models

class Transaction(models.Model):

    CHOICES = (
        ('btc', 'BTC'),
        ('eth', 'ETH'),
    )

    STATES = (
        ('processing', 'PROCESSING'),
        ('success', 'SUCCESS'),
        ('failed', 'FAILED'),
    )

    transaction_ref = models.CharField(max_length=255, default="demo1234")
    currency_amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency_type = models.CharField(max_length=255, choices=CHOICES)
    source_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='source_user')
    target_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='target_user')
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_upated = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=255, choices=STATES, default="processing")
    
    def __str__(self):
        return ("Transaction of {} made by {} on: {}".format(currency_amount, source_user, timestamp_created))