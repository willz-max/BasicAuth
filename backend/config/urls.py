from django.urls import path, include

urlpatterns=[
    path('auth/', include('modules.auth.auth_urls')),
]