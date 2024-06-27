from django import http
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import *
from django.contrib.auth import *


@csrf_exempt    #在django中通过ajax发起请求，需要在对应请求的视图函数加上@csrf_exempt装饰器，禁用csrf_token验证
def login(request):
    """不直接通过表单获取提交的数据，而是通过js获取并校验后通过ajax提交到服务器端（对应的视图函数）"""
    if request.method == 'POST':
        # print('username:', request.POST.get('loginName'))
        # print('password:', request.POST.get('loginPwd'))

        username = request.POST.get('loginName')
        password = request.POST.get('loginPwd')

        # 判断是否有该用户
        user = User.objects.filter(username=username).exists()
        if not user:
            # ajax发起的请求，所以需要数据返回给ajax跳转页面而不能直接在视图函数使用redirect
            # 跳转页面
            return http.JsonResponse({'msg': 'login failed', 'code': 404, 'redirectUrl': 'http://localhost:8001/account/login?error=the user is not exist...'})

        user = authenticate(username=username, password=password)
        if not user:
            return http.JsonResponse({'msg': 'login failed', 'code': 404, 'redirectUrl': 'http://localhost:8001/account/login?error=the username or the password error...'})
        return http.JsonResponse({'msg': 'login success', 'code': 200, 'redirectUrl': 'http://localhost:8001/dashboard/index'})
    else:
        error = request.GET.get('error')
        return render(request, 'account/login.html', {
            'error': error
        })
