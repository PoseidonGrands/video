from django.shortcuts import render, redirect
from django.contrib.auth.models import *
from django.urls import reverse


def index(request):
    """进入该页面需要校验：1、是否登录 2、用户是否有权限访问"""
    print('login username: ', request.user)
    _user = request.user
    users = User.objects.all()
    if _user not in users:
        return redirect('/account/login?error=the user is not invalid...')

    return render(request, 'dashboard/index_base.html')

def admin_manager(request):
    return render(request, 'dashboard/manager_admin.html')

def admin_user(request):
    return render(request, 'dashboard/manager_user.html')

def admin_video(request):
    return render(request, 'dashboard/manager_video.html')

