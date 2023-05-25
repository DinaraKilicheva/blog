from datetime import timedelta

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from config import settings
from users.models import User, VerificationCode
from users.serializers import (
    UserSerializer,
    UserDetailSerializer,
    RegisterSerializer,
    CustomRegisterTokenSerializer,
    SendEmailVerificationCodeSerializer,
    CheckEmailVerificationCodeSerializer
)


# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=UserDetailSerializer)
    def put(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterTokenView(TokenObtainPairView):
    serializer_class = CustomRegisterTokenSerializer


class SendEmailVerificationCodeView(APIView):
    
    @swagger_auto_schema(request_body=SendEmailVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = get_random_string(allowed_chars="0123456789", length=6)
        verification_code, _ = (
            VerificationCode.objects.update_or_create(email=email, defaults={"code": code, "is_verified": False})
        )
        verification_code.expired_at = verification_code.last_sent_time + timedelta(seconds=30)
        verification_code.save(update_fields=["expired_at"])
        subject = "Email registration"
        message = f"Your  email confirm code: {code}"
        send_mail(
            subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
        )
        return Response({"detail": "Successfully sent email verification code."})


class CheckEmailVerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = CheckEmailVerificationCodeSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        verification_code = self.get_queryset().filter(email=email, is_verified=False).order_by(
            "-last_sent_time").first()
        if verification_code and verification_code.code != code and verification_code.is_expire:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification code is verified."})