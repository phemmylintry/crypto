from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

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

    currency_amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency_type = models.CharField(max_length=255, choices=CHOICES)
    source_user_id = models.ForeignKey(User, related_name='source_user', on_delete=models.CASCADE)
    target_user_id = models.ForeignKey(User, related_name='target_user', on_delete=models.CASCADE)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_upated = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=255, choices=STATES)