from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

User = get_user_model()


# verify user by jwt token after sending email
class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")
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
        user_obj = User.objects.get(pk=user_id)
        # if user is already verified
        if user_obj.is_verified:
            return Response(
                {"detail": "Your account has alreadey been verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj.is_verified = True
        user_obj.is_active = True
        user_obj.save()
        return Response(
            {
                "detail": "Your account has been verified and activated successfully."
            },
            status=status.HTTP_200_OK,
        )
