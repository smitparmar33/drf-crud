# from django.contrib.auth.models import User
import email
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer,SignupSerializer,Usererializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
from django.contrib.auth.hashers import check_password
from django.db.models import Q


# from movies.models import User

from django.contrib.auth import get_user_model,authenticate
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

def generateToken(user):
    token=RefreshToken.for_user(user)
    return Response({
        # 'token': token.key,
        
        "refresh":str(token),
        "access": str(token.access_token),
        'user_id': user.pk,
        'email': user.email
    })
            
class CustomAuthToken(ObtainAuthToken): #Custom authentication to login with email,mobile,password and otp
    serializer_class=Usererializer
    def post(self, request, *args, **kwargs):
    
        otp=request.data.get("otp")
        email=request.data.get("email")
        mobile=request.data.get("phone")
        if otp is None:
    
            try:
                user=User.objects.get( Q(email=email) | Q(phone=mobile))
            except:
                raise exceptions.AuthenticationFailed(('Invalid username/password.'))
            check=check_password(request.data["password"],user.password)

            if check:
                # token, created = Token.objects.get_or_create(user=user)
                return generateToken(user)
            else:
                raise exceptions.AuthenticationFailed(('Invalid username/password.'))