from simple_app.views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', index),
]