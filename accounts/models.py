from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from common.models import BaseModel

from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.email)
