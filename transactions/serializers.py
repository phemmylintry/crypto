from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.http import request
from django.core.exceptions import ObjectDoesNotExist

from .models import Transaction

User = get_user_model()

class TransactionSerializer(serializers.ModelSerializer):

    currency_amount = serializers.DecimalField(required=True, max_digits=18, decimal_places=10)
    currency_type = serializers.ChoiceField(required=True, choices=Transaction.CHOICES)
    target_user = serializers.CharField(required=True, max_length=255)
    source_user = serializers.ReadOnlyField(source='source_user.email')
    transaction_ref = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = Transaction
        fields = ('id', 
                'currency_amount', 
                'currency_type', 
                'source_user', 
                'target_user', 
                'state', 
                'transaction_ref')
    
    def validate(self, attrs):
        currency_amount = attrs.get('currency_amount', None)
        target_user = attrs.get('target_user', None)
        currency_type = attrs.get('currency_type', None)

        user = self.context['request'].user

        get_user = User.objects.get(email=user)
        if currency_type == 'btc':       
            currency_balance = get_user.btc_wallet_balance
        else:
            currency_balance = get_user.eth_wallet_balance


        if currency_balance < currency_amount:
            raise serializers.ValidationError("You do not have enough balance to perform this transaction")
            
        try:
            check_target_id = User.objects.get(id=target_user)
        except User.DoesNotExist:
            raise serializers.ValidationError("The account you're sending too is not a valid user")
    
        return attrs