from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from ..serializers import ChangePasswordApiSerializer

User = get_user_model()


# change password view
class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ChangePasswordApiSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old Password": "Wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user wiil get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
