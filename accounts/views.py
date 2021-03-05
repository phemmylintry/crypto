from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth import get_user_model
from django.http import Http404

from .serializers import UserSerializer, UserLoginSerializer, AccountBalanceSerializer

User = get_user_model()


class UserCreateView(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()

        if not user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class UserDetailView(APIView):

    permission_classes = (IsAuthenticated, )
    authenctication_classes = (TokenAuthentication, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format='json'):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountBalanceView(APIView):

    permission_classes = [IsAuthenticated]
    authenctication_classes = (TokenAuthentication, )


    def get(self, request, format='json'):

        user = request.user.id
        account_balance = User.objects.get(id=user)
        
        serializer = AccountBalanceSerializer(account_balance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return Response({
            "status" : "Logged in successfully",
            "data" : serializer.data
            }, status=status.HTTP_201_CREATED)