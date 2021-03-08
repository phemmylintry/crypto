from rest_framework import serializers
from rest_framework import validators
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate

from decimal import Decimal


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True,
                                validators = [validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8)
    btc_wallet_address = serializers.CharField(required=True)
    eth_wallet_address = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 
                'fullname', 
                'password', 
                'email', 
                'btc_wallet_address',
                'eth_wallet_address',
                )
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AccountBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'btc_wallet_balance', 'eth_wallet_balance')


class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

    
    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if not email or not password:
            raise serializers.ValidationError("Please enter email address or password")
            
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Wrong email or password")

        if not user.is_active:
            raise serializers.ValidationError("User is not active, Please contact administrator")

        token, created = Token.objects.get_or_create(user=user)
        attrs['token'] = token.key
        
        return attrs





