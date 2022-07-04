from django.urls import path
from authentication.views import CustomAuthToken, RegisterView, SignupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('signup/', SignupView.as_view(), name='auth_signup'),
    path('api-token-auth/', CustomAuthToken.as_view()),
]