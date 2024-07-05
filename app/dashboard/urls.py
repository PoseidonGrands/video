from django.urls import path
from .views_admin import *
from .views_video import *

urlpatterns = [
    path('index', index, name='dashboard_index'),
    path('manage/admin', admin_manager, name='dashboard_admin'),
    # page_index是跳转前的页码
    path('manage/admin/<str:page_opt>/<str:page_index>', admin_manager, name='dashboard_admin'),
    path('manage/user', admin_user, name='dashboard_user'),
    path('manage/video_external', video_external, name='video_external'),
    # 外链视频信息编辑
    path('manage/video_external_edit/<int:video_id>', video_external_edit, name='video_external_edit'),
    path('manage/video_custom', video_custom, name='video_custom'),
    path('manage/video_detail/<int:video_id>', video_detail, name='video_detail'),
    path('manage/video_detail/<int:video_id>/<str:current_page>/', video_detail, name='video_detail'),
    path('manage/video_detail/<int:video_id>/<str:current_page>/<str:page_opt>', video_detail, name='video_detail'),
    path('manage/video_detail_performer/<int:video_id>', video_detail_performer, name='video_detail_performer'),
    path('manage/video_detail_performer_del/<int:video_id>', video_detail_performer_del, name='video_detail_performer_del'),
    # 集数信息编辑
    path('manage/video_detail_episode_edit/', video_detail_episode_edit, name='video_detail_episode_edit'),
    path('manage/video_detail_episode_del/<int:video_id>/<int:video_sub_id>', video_detail_episode_del, name='video_detail_episode_del'),
]