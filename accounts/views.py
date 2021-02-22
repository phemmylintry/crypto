from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer, UserLoginSerializer



class UserCreateView(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()

        if not user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return Response({
            "status" : "Logged in successfully",
            "data" : serializer.data
            }, status=status.HTTP_201_CREATED)