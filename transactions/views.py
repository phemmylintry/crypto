from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model

from .serializers import TransactionSerializer
from .models import Transaction
from .tasks import send_transaction

import uuid

User = get_user_model()

class TransactionView(generics.CreateAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authenctication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        currency_type = serializer.validated_data['currency_type']

        target_user = serializer.validated_data['target_user']
        get_target_user = User.objects.get(id=target_user)

        #generate randome key for transaction token
        transaction_ref = uuid.uuid4()

        source_user = self.request.user

        send_transaction.delay()

        return serializer.save(source_user=source_user, 
                        currency_type=currency_type, 
                        target_user=get_target_user, 
                        transaction_ref=transaction_ref)
        
