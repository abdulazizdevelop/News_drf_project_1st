from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import User
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.response import Response
from .utility import check_email

class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True)
    # email= serializers.EmailField(unique= True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
    
    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise   ValidationError({"password": "Password fields didn't match"})
        
        return attrs

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            data = {
                'status': False, 
                'message': 'username already exist!'
            }
            raise ValidationError(data)

        return username
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
        )

        user.set_password(validated_data["password1"])
        user.save()

        return user
class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, data) :
        username = data.get('username')
        password = data.get('password')
        
        auth_kwargs = {self.username_field: username, 'password': password}
        user = authenticate(**auth_kwargs)
        
        if user is not None:
            self.user = user
            
        else:
            data = {
                'status': False,
                'message': 'password or username is wrong  '
            }
            raise ValidationError(data)
        data = self.user.token()
        data['username']=username
        return data
        
class UpdateTokenSerializer(TokenRefreshSerializer) :
    
    def validate(self, data):
        data = super().validate(data)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user=user)
        return data
    
    
class LogoutSerializer(serializers.Serializer):
    
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        
         self.token = attrs['refresh']
         return  attrs
    
    def save(self, **kwargs):
        
        try:
            
            RefreshToken(self.token).blacklist()
            
            # data={
            #     'status': True,
            #     'message': 'You have not existed !!!!!'
                
            # }
        
            # return Response(data)
            
        except:
            data={
                'status': True,
                'message': 'You have not existed  !!!!!'
                
            }
            self.fail(data)
            
# from rest_framework import serializers
# from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    
# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField(write_only = True, required=True)

#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#         if check_email(attrs['email']):
#             if User.objects.filter(email = attrs['email']).exists():
#                 return attrs
#             else:
#                 data = {
#                     'status' : False,
#                     'message' : 'There is not user via this email'
#                 } 
#                 raise ValidationError(data)
#         data = {
#             'status' : False,
#             'message' : 'are you sure you typed email bro?'
#         }
#         raise ValidationError(data)

# class PasswordResetViaCodeSerializer(serializers.Serializer):
#     password1 = serializers.CharField(write_only = True, validators = [validate_password])
#     password2 = serializers.CharField(write_only = True)
#     code = serializers.CharField(write_only = True, required = True)

#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#         if attrs['password1'] != attrs['password2']:
#             data = {
#                 'status' : False,
#                 'message' : 'passwords are not equal!'
#             }
#             raise ValidationError(data)
#         return attrs





class PasswordResetSerializer2(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields=("email", )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

            
        
            
            
            
            
            
            
        
        
        
        
        
    
         