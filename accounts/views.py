from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from .serializers import UserSerializer, LoginSerializer


class SignupView(APIView):
    def post(self, request):
        data = request.data
        user = UserSerializer(data=data)

        if not user.is_valid():
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(**user.validated_data)

        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)

        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = LoginSerializer(data=data)

        if not user.is_valid():
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=user.validated_data["username"],
            password=user.validated_data["password"]
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
        
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
