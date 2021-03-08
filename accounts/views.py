from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from django.contrib.auth import get_user_model
from django.http import Http404

from .serializers import UserSerializer, UserLoginSerializer, AccountBalanceSerializer
from .permissions import IsAdmin

User = get_user_model()


class UserCreateView(APIView):


    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
    )
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

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def get(self, request, format='json'):
        user = request.user.id

        try:
            get_user = User.objects.get(id=user)
        except User.DoesNotExist:
            return Response({
                "status" : "Failed",
                "data" : {
                    "messgae" : "Invalid request"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(get_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountBalanceView(APIView):

    permission_classes = [IsAuthenticated]
    authenctication_classes = (TokenAuthentication, )

    @extend_schema(
        request=AccountBalanceSerializer,
        responses={201: AccountBalanceSerializer},
    )
    def get(self, request, format='json'):

        user = request.user.id
        account_balance = User.objects.get(id=user)
        
        serializer = AccountBalanceSerializer(account_balance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginView(ObtainAuthToken):

    @extend_schema(
        request=UserLoginSerializer,
        responses={201: UserLoginSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return Response({
            "status" : "Logged in successfully",
            "data" : serializer.data
            }, status=status.HTTP_201_CREATED)



class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authenctication_classes = (TokenAuthentication, )

