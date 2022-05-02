from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user/avatars/', null=True, blank=True)

    def serialize_jwt_pair_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
