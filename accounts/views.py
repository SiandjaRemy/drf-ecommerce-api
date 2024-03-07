from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import SignUpSerializer, LoginSerializer
from .tokens import create_jwt_pair_for_user
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


# Test other types of Apis here too
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User created Succesfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]


    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)
            
            response = {
                "message": "Login Successfull",
                "tokens": tokens
            }

            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data={"message":"Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
    # def get(self, request: Request):
    #     content = {
    #         "user": str(request.user),
    #         "token": str(request.auth),
    #     }

    #     return Response(data=content, status=status.HTTP_200_OK)


class LoginGenericView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
            operation_summary="Login user"
    )
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = authenticate(email=email, password=password)

            if user is not None:

                tokens = create_jwt_pair_for_user(user)

                response = {
                    "message": "Login succesfull",
                    "tokens": tokens
                }

                return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data={"message":"Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)



