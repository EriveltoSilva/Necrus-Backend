import random 
import shortuuid
from .models import User, Profile
from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


def generate_otp(length=12):
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]

class PasswordResetEmailVerifyView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp = generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp
            link = f'http://localhost:5173/create-new-password?otp={otp}&uid64={uidb64}'

            # Send email do user with link 
            print("#"*100)           
            print('Clique aqui:',link)
            print("#"*100)           

        return user