from rest_framework import serializers
from rest_framework import validators
from django.contrib.auth import get_user_model
from decimal import Decimal
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    # description = serializers.CharField()
    email = serializers.EmailField(required=True,
                                validators = [validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8)
    # btc_wallet_amount = serializers.DecimalField(default=0, max_digits=18, decimal_places=10, min_value=0, max_value=1000000000)
    btc_wallet_address = serializers.CharField(required=True)
    # eth_wallet_amount = serializers.DecimalField(default=0, max_digits=18, decimal_places=10, min_value=0, max_value=1000000000)
    eth_wallet_address = serializers.CharField(required=True)
    # max_amount_per_transaction = serializers.DecimalField(default = Decimal('10000.00'), max_digits=6, decimal_places=2)

    class Meta:
        model = User
        fields = ('id', 
                'name', 
                # 'description',
                'password', 
                'email', 
                # 'btc_wallet_amount',
                'btc_wallet_address',
                # 'eth_wallet_amount',
                'eth_wallet_address',
                # 'max_amount_per_transaction'
                )
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user






