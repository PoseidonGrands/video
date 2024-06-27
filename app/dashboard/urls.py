from django.urls import path
from .views import *

urlpatterns = [
    path('index', index, name='dashboard_index'),
    path('manage/admin', admin_manager, name='dashboard_admin'),
    path('manage/user', admin_user, name='dashboard_user'),
    path('manage/video', admin_video, name='dashboard_video'),

]