from django.urls import path
from .views import *
from .views_auth import *

urlpatterns = [
    path('', index, name='index'),
    path('external_video', client_external_video, name='client_external_video'),
    path('custom_video', client_custom_video, name='client_custom_video'),
    path('video/<int:video_id>', client_video_detail, name='client_video_detail'),
    path('mine', mine, name='mine'),
    path('login', client_login, name='client_login'),
    path('reg', client_reg, name='client_reg'),
    path('logout', client_logout, name='client_logout'),

]