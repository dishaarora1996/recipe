from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from .serializers import (ChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, 
                          UserLoginSerializer)
from employee.utils import validate_email
from rest_framework.generics import GenericAPIView
from employee.models import Operator

import logging
logger = logging.getLogger(__name__)



class AuthorizedOnly(generics.GenericAPIView):

   
    permission_classes= [IsAuthenticated,]
    serializer_class=UserLoginSerializer

    def post(self,req ):

        logger.info(f"Request data :{req.data}")

        return Response("Welcome authorized user : "+req.user.username)

            

logger = logging.getLogger(__name__)

invalid_email_password = "Invalid Email or Password"
invalid_email_id = "Please provide valid email id"

login_response_schema_dict = {
    "200": openapi.Response(
        description="Login Successfull"
    ),
    "401": openapi.Response(
        description=invalid_email_password
    ),
    "400": openapi.Response(
        description=invalid_email_id
    )
}


class UserLoginView(TokenObtainPairView):
    ''' User Login '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Login url to get access token", operation_summary="Login",
                         request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email','password'],
        properties={
            'email':openapi.Schema(type=openapi.TYPE_STRING),
            'password':openapi.Schema(type=openapi.TYPE_STRING)
        },
    ), responses=login_response_schema_dict)
    def post(self, request):
        ''' User Login '''
        serializer = UserLoginSerializer()
        login_response = {}
        http_status = None
        
        username = request.data.get('email')
        password = request.data.get('password')
        if not validate_email(username):
            login_response['error'] = invalid_email_id
            http_status = status.HTTP_400_BAD_REQUEST
            return Response(login_response, status=http_status)

        user_data = {"username": username, "password": password}
        user = authenticate(
            username=username, password=password)
        logger.info("User : %s", user)
        if user:
            logger.info("Valid User")
            serializer_data = serializer.validate(attrs=user_data)
            logger.info("Serializer Data : %s ", serializer_data)
            login_response = serializer_data
            http_status = status.HTTP_200_OK
        else:
            logger.info("Invalid User")
            login_response['error'] = invalid_email_password
            http_status = status.HTTP_401_UNAUTHORIZED
        return Response(login_response, status=http_status)



class ChangePassword(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Reset Password", operation_summary="Reset Password", request_body=ChangePasswordSerializer)
    def put(self, request):
        data = request.data
        response = {}
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        user_id = data.get('user_id')

        if new_password == confirm_password:
            if current_password != confirm_password:
                user_id_validate = User.objects.filter(id=data.get('user_id'))
                if user_id_validate.exists():
                    if check_password(current_password, User.objects.get(
                            id=user_id).password):
                        user_name = user_id_validate.first().username
                        user_id_validate.update(
                            password=make_password(confirm_password))
                        Operator.objects.filter(
                            NM_USR=user_name).update(PW_ACS_OPR=confirm_password)
                        response["message"] = 'Password Changed successfully'
                        http_status = status.HTTP_200_OK
                    else:
                        response["message"] = 'Current Password Is Invalid'
                        http_status = status.HTTP_400_BAD_REQUEST
                else:
                    response["message"] = 'Invalid User Id'
                    http_status = status.HTTP_400_BAD_REQUEST
            else:
                response["message"] = "Old password and New Password can't be Same"
                http_status = status.HTTP_400_BAD_REQUEST
        else:
            response["message"] = "New password and Confirm Password mismatch"
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(response, status=http_status)
    

class SendPasswordResetEmailView(generics.GenericAPIView):
    serializer_class=SendPasswordResetEmailSerializer
    
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset link send. Please check your email.'},
                             status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserPasswordResetView(generics.GenericAPIView):
    serializer_class=UserPasswordResetSerializer

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, 
                                                 context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    