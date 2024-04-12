from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'referral_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validators(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password & confirm doesn't match")
        return data

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        user = User.objects.create_user(**validated_data)

        # Check if a referral code is provided
        if referral_code:
            try:
                referred_user = User.objects.get(referral_code=referral_code)
                user.referral = referred_user
                user.save()
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code")

        return user


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
