from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(
            self,
            username: str,
            email: str,
            name: str,
            last_name: str,
            password: str,
            is_staff: bool,
            is_superuser: bool,
            **extra_fields
    ) -> AbstractBaseUser:

        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
            self,
            username: str,
            email: str,
            name: str,
            last_name: str,
            password: str,
            **extra_fields
    ) -> AbstractBaseUser:

        return self._create_user(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            password=password,
            is_staff=False,
            is_superuser=False,
            **extra_fields
        )

    def create_superuser(
            self,
            username: str,
            email: str,
            name: str,
            last_name: str,
            password: str,
            **extra_fields
    ) -> AbstractBaseUser:

        return self._create_user(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('email', max_length=255, unique=True,)
    name = models.CharField('name', max_length=255, blank=True, null=True)
    last_name = models.CharField('last_name', max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username} {self.email}'
