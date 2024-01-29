from django.urls import path
from .views import (SignupApiView,
                    LoginApiView,
                    UpdateTokenApiview,
                    LogoutApiView , 
                    ChangePasswordView,
                    #PasswordResetView, 
                    #PasswordResetViaCodeView,
                    PasswordResetApiView,
                    PasswordResetConfirmView)


urlpatterns =[
    path('signup/', SignupApiView.as_view()),
    path('login/',LoginApiView.as_view()),
    path('update_token/', UpdateTokenApiview.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('password_change/', ChangePasswordView.as_view()),
    # path('password_update_sent_email/' , PasswordResetView.as_view()),
    # path('password_update_finish/', PasswordResetViaCodeView.as_view()),
    path('password_reset/', PasswordResetApiView.as_view()),
    path('password_confirm/', PasswordResetConfirmView.as_view())
]
