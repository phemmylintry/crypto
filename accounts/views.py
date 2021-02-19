from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserSerializer



class UserCreateView(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()

        if not user:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = Token.objects.create(user=user)
        json = serializer.data
        json['token'] = token.key


        return Response(json, status=status.HTTP_201_CREATED)