from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView,  RegisterTokenView, ProfileView, SendEmailVerificationCodeView, \
    CheckEmailVerificationCodeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/token/', RegisterTokenView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email/verification/', SendEmailVerificationCodeView.as_view(), name='send-email-code'),
    path('email/check-verification/', CheckEmailVerificationCodeView.as_view(), name='check-email-code'),
    # path('auth/google/', GoogleLogin.as_view(), name='google_auth'),
    # path('auth/facebook/', FacebookLogin.as_view(), name='facebook_auth'),
]
