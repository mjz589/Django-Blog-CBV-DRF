from rest_framework import generics
from django.conf import settings
import jwt
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsNotAuthenticated
from ..serializers import ResetPasswordTokenSerializer


# errors
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from django.contrib.auth import get_user_model

User = get_user_model()


# Reset password by jwt token after sending email
class ResetPasswordTokenApiView(generics.GenericAPIView):
    model = User
    permission_classes = [
        IsNotAuthenticated,
    ]
    serializer_class = ResetPasswordTokenSerializer
    lookup_url_kwarg = "token"

    # Reset password by user_id given by jwt token
    def put(self, request, token, *args, **kwargs):
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
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        # set_password also hashes the password that the user will get
        user_obj.set_password(serializer.data.get("password1"))
        user_obj.save()
        return Response(
            {"details": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )
