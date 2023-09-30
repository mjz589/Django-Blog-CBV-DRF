from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..serializers import ResetPasswordSerializer
from ..permissions import IsNotAuthenticated

# email
from mail_templated import EmailMessage
from ...utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

User = get_user_model()


# Reset Password Request view
class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [
        IsNotAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/reset_password.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        data = {
            "detail": "Please check your email and click the link to Reset your password.",
            "email": user_obj.email,
        }
        # multi threading
        EmailThread(email_obj).start()
        return Response(data, status.HTTP_200_OK)

    # get access token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
