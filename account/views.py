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

# Function to Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# User Registration View


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'message': 'Registration Success!', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', 'token': token}, status=status.HTTP_200_OK)
            else:

                return Response({'errors': {'non_field_errors': ['Email or Password is Incorrect']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        # if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=status.HTTP_200_OK)


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

        return Response({'msg': "Patch Update Success!"}, status=status.HTTP_200_OK)
