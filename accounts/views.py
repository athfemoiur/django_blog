from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import RegisterSerializer, UserInfoSerializer, UserChangePasswordSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class UserInfoView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class UserInfoUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class UserChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserChangePasswordSerializer

    def get_object(self):
        return self.request.user
