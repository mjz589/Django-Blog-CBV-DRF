from django.urls import path, include

# from .views import *


app_name = "accounts"

urlpatterns = [
    # path('login' , login_view, name='login'),
    # path('logout', logout_view, name='logout'),
    # path('signup' , signup_view, name='signup'),
    # path('forget-password/',forget_password_view, name='forget-password'),
    # path('reset-password/<token>/', reset_password_view, name='reset-password'),
    path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("accounts.api.v1.urls")),
]
