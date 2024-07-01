from django.urls import path
from .views_admin import *
from .views_video import *

urlpatterns = [
    path('index', index, name='dashboard_index'),
    path('manage/admin', admin_manager, name='dashboard_admin'),
    # 这里的page_index是跳转前的页码
    path('manage/admin/<str:page_opt>/<str:page_index>', admin_manager, name='dashboard_admin'),
    path('manage/user', admin_user, name='dashboard_user'),
    path('manage/video_external', video_external, name='video_external'),
    path('manage/video_custom', video_custom, name='video_custom'),

]