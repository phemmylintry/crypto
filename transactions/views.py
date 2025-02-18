from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import get_user_model

from django_q.tasks import async_task, result

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .serializers import TransactionSerializer, TransactionListSerializer
from .models import Transaction
from .tasks import send_transaction

import uuid

User = get_user_model()

class TransactionView(generics.CreateAPIView):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    authenctication_classes = (TokenAuthentication, )

    @extend_schema(
        request=TransactionSerializer,
        responses={201: TransactionSerializer},
    )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        transaction = self.perform_create(serializer)

        if transaction == "success":
            get_transaction_id = serializer.data['transaction_ref']
            transact = Transaction.objects.get(transaction_ref=get_transaction_id)
            transact.state = "success"
            transact.save(update_fields=['state'])
        else:
            return Response ({
                'status' : "Tansaction not succesful",
                'data' : {
                    'transaction_ref' : serializer.data['transaction_ref']
                }
            })
        
        #update transaction state :(
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

        task = async_task('transactions.tasks.send_transaction', source_user, target_user, currency_type, transfer_amount)
        # task = send_transaction.apply_async((source_user, target_user, currency_type, transfer_amount), countdown=2)
        results = result(task, 200)
        print(results)
        return results



class TransactionListView(APIView):

    permission_classes = (IsAuthenticated, )
    authenctication_classes = (TokenAuthentication, )

    @extend_schema(
        request=TransactionListSerializer,
        responses={201: TransactionListSerializer},
    )
    def get(self, request, format='json'):

        user = request.user.id
        
        if not user:
            return Response({
                "status" : "Error",
                "data" : {
                    "message" : "Invalid user"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        transactions = Transaction.objects.all()

        data = []

        for items in transactions:
            
            if items.source_user_id == user or items.target_user_id == user:
            
                data.append({
                    'transaction_ref' : items.transaction_ref,
                    'currency_amount' : items.currency_amount,
                    'currency_type' : items.currency_type,
                    'source_user_id' : items.source_user_id,
                    'target_user_id' : items.target_user_id,
                    'state' : items.state,
                    'time_of_transaction': items.timestamp_created
                })

        
        if data == []:
            return Response(
                {
                    "data" : "No transaction history"
                }, status=status.HTTP_200_OK)
        
        return Response(data, status=status.HTTP_200_OK)
        