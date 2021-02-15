from django.db import models

# Create your models here.
import os
from uuid import uuid4
from django.utils import timezone


class Cfuser(models.Model):
    email = models.EmailField(verbose_name='이메일')
    name = models.CharField(max_length=20, verbose_name='이름')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    phone = models.CharField(max_length=50, verbose_name='전화번호')
    level = models.CharField(max_length=8, verbose_name='등급',
        choices=(
            ('admin', 'admin'),
            ('user', 'user')
        ))
    image = models.ImageField(blank=True, null=True, upload_to="images", default='profile.png')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'coffeeshop'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
