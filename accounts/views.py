from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ipdb import set_trace
from django.db import IntegrityError




class SignupView(APIView):
    def post(self, request):
        try:
            user = User.objects.create_user(
                username=request.data['username'], 
                password=request.data['password'],
                is_staff=request.data.pop('is_staff', False),
                is_superuser=request.data.pop("is_superuser", False)
            )

        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {   "id": user.id,
                "username": user.username,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
            }, 
            status=status.HTTP_201_CREATED
        )



class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(
            username=username, 
            password=password
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
        
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user.__dict__)
        
        return Response({"message": "Welcome"}, status=status.HTTP_200_OK)