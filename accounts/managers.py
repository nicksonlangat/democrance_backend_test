from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be staff.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be superuser")

        return self.create_user(email, password, **extra_fields)
