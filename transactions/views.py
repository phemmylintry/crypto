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

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        transaction = self.perform_create(serializer)
        get_transaction_id = transaction['transaction_ref']
        
        transact = Transaction.objects.get(transaction_ref=get_transaction_id)
        
        transact.state = "obj"
        transact.save(update_fields=['state'])

        headers = self.get_success_headers(serializer.data)
        return Response({
                    'status' : "Transaction is successful.",
                    'data' : {
                        'transaction_ref' : serializer.data['transaction_ref']
                    }
                }, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        currency_type = serializer.validated_data['currency_type']

        target_user = serializer.validated_data['target_user']
        get_target_user = User.objects.get(id=target_user)
        serializer.validated_data['target_user'] = get_target_user

        #generate randome id for transaction token
        transaction_ref = uuid.uuid4()
        serializer.validated_data['transaction_ref'] = transaction_ref

        source_user = self.request.user
        serializer.validated_data['source_user'] = source_user

        serializer.save()

        target_user = serializer.data['target_user']
        source_user = serializer.data['source_user']
        currency_type = serializer.data['currency_type']
        transfer_amount = serializer.data['currency_amount']

        task = send_transaction.delay(source_user, target_user, currency_type, transfer_amount)

        return serializer.data