from .utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from rest_framework import serializers
from employee.models import Operator, WorkerOperatorAssignment, Employee

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserLoginSerializer(TokenObtainPairSerializer):
    ''' Login Serializer '''
    username = serializers.CharField(
        max_length=255, min_length=5, allow_blank=False)
    password = serializers.CharField(
        max_length=40, min_length=8, allow_blank=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        username=self.user.username

        # Get User Timezone
        if not self.user.is_superuser:
          worker_operator = WorkerOperatorAssignment.objects.filter(ID_OPR__NM_USR=username).first()
          if worker_operator:
            employee = Employee.objects.filter(ID_WRKR=worker_operator.ID_WRKR).first()
            data['timezone'] = employee.TZ_EM.GMT_OFST
        else:
            data['timezone'] = "default_timezone_for_superuser"
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['email'] = username
        data['id'] = self.user.pk
        data['is_superuser'] = self.user.is_superuser
        return data




class ChangePasswordSerializer(serializers.Serializer):
    '''Change PAssword Serializer'''

    user_id = serializers.IntegerField(required=True)
    current_password = serializers.CharField(
        max_length=20, allow_blank=False, )
    new_password = serializers.CharField(
        max_length=20, allow_blank=False,)
    confirm_password = serializers.CharField(
        max_length=20, allow_blank=False,)


class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      link = f'http://localhost:3000/api/user/reset/{uid}/{token}'
      print(f'link: {link}')
      data = {
        'subject': 'Reset Your Password',
        'body': f'Click following link to reset your password {link}',
        'to_email': user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError("You are not a registered user")


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password does not match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError("Token is not valid or expired")


      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not valid or expired')



