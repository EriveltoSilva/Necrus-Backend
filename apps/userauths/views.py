from .models import User, Profile
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
from . import utils

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer




class PasswordResetEmailVerifyView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp = utils.generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp
            link = f'http://localhost:5173/create-new-password?otp={otp}&uid64={uidb64}'

            # Send email do user with link 
            print("#"*100)           
            print('Clique aqui:',link)
            print("#"*100)           

        return user
    
class PasswordChangeView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data
        otp = payload['otp']
        uidb64 = payload['uidb64']
        # reset_token = payload['reset_token']
        password = payload['password']

        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp=""
            # user.reset_token=""
            user.save()

            return Response( {"status":"success","message": "Palavra-Passe alterada com Sucesso"}, status=status.HTTP_201_CREATED)
        else:
            return Response( {"status":"error","message": "Ocorreu um erro ao alterar a palavra-passe"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
