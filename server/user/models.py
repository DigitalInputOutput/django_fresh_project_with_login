#-*- coding=utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin): 
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,blank=True,null=True)
    login = models.CharField(max_length=16, unique=True)
    verified = models.BooleanField(default=0,verbose_name=_("Email verified"))
    fname = models.CharField(max_length=255,blank=False,null=True,verbose_name=_("Vorname"))
    lname = models.CharField(max_length=255,blank=False,null=True,verbose_name=_('Nachname'))
    sname = models.CharField(max_length=255,blank=False,null=True,verbose_name=_('Sname'))
    password = models.CharField(verbose_name=_('Password'), max_length=128)
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    last_login = models.DateTimeField(auto_now_add=True,verbose_name=_("Last online"),null=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_("Created at"),null=True)
    firma = models.CharField(max_length=60)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['fname','lname','sname','email']

    @property
    def full_name(self):
        return f"{self.fname} {self.lname} {self.sname}"

    def get_short_name(self):
        return self.fname.title()

    def __str__(self):
        return self.fname

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')