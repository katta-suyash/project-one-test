from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from account.models import MyUser


class UserRegistrationSerializers(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2', 'first_name', 'last_name',
                  'mobile_number', 'date_of_birth', 'gender', 'profile_photo']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password Doesn't Match!")
        return attrs

    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = MyUser
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name',
                  'mobile_number', 'date_of_birth', 'gender', 'profile_photo']


class UserProfileUpdateSerializer(serializers.Serializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2', 'first_name', 'last_name',
                  'mobile_number', 'date_of_birth', 'gender', 'profile_photo']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password Doesn't Match!")
        return attrs

    def update(self, instance, validate_data):
        return MyUser.objects.update_user(**validate_data)
