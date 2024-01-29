from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import (SignUpSerializer,
                         LoginSerializer,
                         UpdateTokenSerializer, 
                         LogoutSerializer,
                        ChangePasswordSerializer, 
                        # PasswordResetSerializer, 
                        # PasswordResetViaCodeSerializer,
                        PasswordResetSerializer2,
                        PasswordResetConfirmSerializer
                        )
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from .utility import send_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str

 
# Create your views here.

class SignupApiView(CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    
class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
class UpdateTokenApiview(TokenRefreshView):

    serializer_class = UpdateTokenSerializer

class LogoutApiView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]
    
    def post(self, request):
        
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response(status = status.HTTP_204_NO_CONTENT)
    

        
        
        




class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class PasswordResetView(APIView):
#     permission_classes = (AllowAny, )
#     serializer_class = PasswordResetSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data.get('email')
#         user = get_object_or_404(User, email=email)
#         code = user.create_verify_code()

#         data = {
#             'status' : True,
#             'message' : 'you get email via verify code'
#         }
#         send_email(email, code)
#         return Response(data)

# class PasswordResetViaCodeView(APIView):
    # serializer_class = PasswordResetViaCodeSerializer
    # permission_classes = (AllowAny, )
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     code = serializer.validated_data.get('code')
    #     password = serializer.validated_data.get('password1')
    #     verify_code = User.objects.filter(code_lifetime__gte = datetime.now(), code = code, is_confirmed=False)
    #     if verify_code.exists():
    #         user = verify_code.first().user
    #         user.set_password(password)
    #         user.save()
    #         verify_code.update(is_confirmed = True)
    #         data = {
    #             'status' : True,
    #             'message' : 'password reseted'
    #         }
    #         return Response(data)
    #     data = {
    #         'status' : False,
    #         'message' : 'we can not find this verification code'
    #     }
    #     return Response(data)
    
    
class PasswordResetApiView(APIView):
    serializer_class = PasswordResetSerializer2
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
                send_mail(
                    'Password Reset',
                    f'Use the following link to reset your password: {reset_link}',
                    'abdulazizwh04@gmail.com',
                    [email],
                    fail_silently=False,
                )
                # print(token)

            return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes= [AllowAny,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user_id=force_str(urlsafe_base64_decode(uid))
                user=User.objects.get(pk=user_id)
            except (TypeError, ValueError, OverflowError,  User.DoesNotExist):
                user=None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password muvafaqqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)


    
    
