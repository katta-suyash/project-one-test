from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializers
from account.serializers import UserLoginSerializer
from account.serializers import UserProfileSerializer
from account.serializers import UserProfileUpdateSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import MyUser
from projectone.utility import get_tokens_for_user
from projectone.utility.utils import success_response, error_response, validation_error_response


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializers(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return validation_error_response(errors=e)
        user = serializer.save()
        return success_response(message='Registration Success!', extra_data={"token": get_tokens_for_user(user)})


# User Login View
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = UserLoginSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return validation_error_response(errors=e)

        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            return success_response(message='LOGIN_SUCCESS', extra_data={"token": get_tokens_for_user(user)})
        else:
            return error_response(message='Email or Password is Incorrect', code=400)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        try:
            serializer = UserProfileSerializer(request.user)
        except Exception as e:
            return validation_error_response(errors=e)

        return success_response(data=serializer.data, message='Data Fetched Successfully!')


class UserProfileUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        user = self.request.user
        print("User ID>>>>>", user.id)
        userobject = MyUser.objects.filter(id=user.id).first()
        print("User Object>>>>>", userobject)

        try:
            userobject.firstName = request.data.get(
                "firstName", userobject.firstName)
            userobject.lastName = request.data.get(
                "lastName", userobject.lastName)
            userobject.email = request.data.get("email", userobject.email)
            userobject.mobileNumber = request.data.get(
                "mobileNumber", userobject.mobileNumber)
            userobject.dateOfBirth = request.data.get(
                "dateOfBirth", userobject.dateOfBirth)
            userobject.gender = request.data.get("gender", userobject.gender)
            userobject.profilePhoto = request.data.get(
                "profilePhoto", userobject.profilePhoto)
            userobject.save()
        except Exception as e:
            print(e)
            return error_response(message="Patch Update Success!", code=400)

        return success_response(message="Patch Update Success!")
        # return Response({'msg': "Patch Update Success!"}, status=status.HTTP_200_OK)
