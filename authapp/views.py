from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authapp.serializers import UserRegisterSerializer, UserDetailSerializer, UserProfileSerializer, ReferralSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def generate_jwt_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


# Token Generate Manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    print("in userregistration view")
    def post(self, request, form=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token = get_tokens_for_user(user)
            user_id = serializer.data['id']
            return Response({'user_id': user_id,'msg':'Registeration Success', 'token':token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,form=None):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                name = user.name
                referral_code = user.referral_code
                return Response({'email':email, 'token':token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':'Error occured'}, status=status.HTTP_400_BAD_REQUEST)

class ReferralLoginView(APIView):
    def post(self, request, form=None):
        serializer = ReferralSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            referral_code = serializer.data.get('referral_code')
            user_with_referral = User.objects.filter(referral_code=referral_code)

            if user_with_referral.exists():
                user_data = UserProfileSerializer(user_with_referral, many=True).data
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                return Response({'msg':'No user have referral code'}, status=status.HTTP_404_NOT_FOUND)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, form=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ReferralView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, form=None):
        serializer = ReferralDataSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

