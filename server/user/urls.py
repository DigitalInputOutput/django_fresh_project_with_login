from django.urls import path
from user.views import *

urlpatterns = [
    path('logup', LogupView.as_view(),name='logup'),
    path('login', LoginView.as_view(), name="login"),
    path('logout', logout, name="logout"),
]