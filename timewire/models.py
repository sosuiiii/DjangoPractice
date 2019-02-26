

# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse

# 　　　　新規▼
class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        # 継承▼
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
# 　　　　　継承▼
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Work(models.Model):
    class Meta:
        db_table = 'work'

    name = models.CharField(verbose_name="店舗名", max_length=255)
    price = models.IntegerField(verbose_name="時給")
    content = models.TextField(verbose_name="案件詳細", null=True, blank=True)
    user_id = models.IntegerField(verbose_name="ユーザーID", null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str___(self):
        return self.name

    def get_absolute_url(self):

        return reverse('timewire:index')


class Check(models.Model):
    class Meta:
        db_table = 'check'

    user_id = models.IntegerField(verbose_name='ユーザーID', null=True)
    work_id = models.IntegerField(verbose_name='ジョブID', null=True)

    def __str__(self):
        return self.title