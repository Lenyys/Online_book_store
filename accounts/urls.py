from django.urls import path
from .views import custom_login_view

urlpatterns = [
    path('login/', custom_login_view, name='custom_login'),
]