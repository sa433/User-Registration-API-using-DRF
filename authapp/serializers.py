from rest_framework import serializers
from authapp.models import User
import random
import string


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id','email', 'name', 'password', 'password2', 'referral_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        password = self.initial_data.get('password')
        password2 = self.initial_data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password & confirm don't match")
        return value

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)

        # Generate a 4-digit referral code if not provided
        if not referral_code:
            referral_code = ''.join(random.choices(string.digits, k=4))

        # Check if a user with the same referral code exists
        users_with_referral_code = User.objects.filter(referral_code=referral_code)

        if users_with_referral_code.exists():
            # Create a new user with the existing referral code
            new_user = User.objects.create_user(**validated_data, referral_code=referral_code)
        else:
            # Create a new user with a new referral code
            new_user = User.objects.create_user(**validated_data, referral_code=referral_code)
        return new_user


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=20)
    class Meta:
        model = User
        fields = ['email','password', 'referral_code']

class ReferralSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(max_length=4)
    class Meta:
        model = User
        fields = ['referral_code']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'referral_code']
