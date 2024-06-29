from django.urls import include, path
from .views import *

urlpatterns = [
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('update_user_status/<str:status>/<str:username>', update_user_status, name='update_user_status'),
]