from rest_framework.views import APIView
from django.conf import settings
from rest_framework.reverse import reverse_lazy
import jwt
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsNotAuthenticated


# errors
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from django.contrib.auth import get_user_model

User = get_user_model()


# Cheak if token is valid and send it to reset-password-token
class ResetPasswordConfirmApiView(APIView):
    model = User
    permission_classes = [
        IsNotAuthenticated,
    ]

    # Cheak if token is valid
    def get(self, request, token, *args, **kwargs):
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # if token has been expired
        except ExpiredSignatureError:
            return Response(
                {"detail": "Your token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if token is invalid
        except InvalidSignatureError:
            return Response(
                {"detail": "Your token is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # go for reset password
        data = {
            "detail": "Token is confirmed. Click below link to set a new password.",
            "reset-password-url": reverse_lazy(
                "accounts:api-v1:reset-password-token",
                request=request,
                kwargs={"token": token},
            ),
        }
        return Response(data)
