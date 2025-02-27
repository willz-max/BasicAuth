from django.urls import path
from modules.auth.auth_views import register

urlpatterns=[
    path(
        'register/', register, name='register'
    ),
]