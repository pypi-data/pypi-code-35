from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser as BaseUser
from django.db import models
from django.db.models import Q

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class AbstractUser(BaseModel, BaseUser):
    """
    用户表
    """
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('GA', 'GroupAdmin'),
        ('CU', 'CommonUser'),
    )
    userid = models.CharField(max_length=32, primary_key=True, auto_created=True)
    QQ = models.CharField(max_length=32, default='', unique=True, blank=True, null=True)
    telephone = models.CharField(max_length=15, unique=True)
    sex = models.CharField(max_length=1, default='F')
    realname = models.CharField(max_length=32, default=None)
    IDcard = models.CharField(max_length=19, default=None, null=True, blank=True, unique=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        abstract = True