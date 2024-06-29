from django import http
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import *
from django.contrib.auth import *


@csrf_exempt    #在django中通过ajax发起请求，需要在对应请求的视图函数加上@csrf_exempt装饰器，禁用csrf_token验证
def user_login(request):
    """不直接通过表单获取提交的数据，而是通过js获取并校验后通过ajax提交到服务器端（对应的视图函数）"""
    if request.method == 'POST':
        # print('username:', request.POST.get('loginName'))
        # print('password:', request.POST.get('loginPwd'))

        username = request.POST.get('loginName')
        password = request.POST.get('loginPwd')
        # 是否存在需要跳转的url
        to_url = request.POST.get('toUrl')
        success_redirect_url = to_url if to_url != '' else 'http://localhost:8001/dashboard/index'
        fail_redirect_url = f'http://localhost:8001/account/login?to={to_url}&' if to_url != '' else 'http://localhost:8001/account/login?'

        # 判断是否有该用户
        user = User.objects.filter(username=username).exists()
        if not user:
            # ajax发起的请求，所以需要数据返回给ajax跳转页面而不能直接在视图函数使用redirect
            # 跳转页面
            return http.JsonResponse({'msg': 'login failed', 'code': 404, 'redirectUrl': fail_redirect_url + 'error=the user is not exist...'})

        user = authenticate(username=username, password=password)
        if not user:
            return http.JsonResponse(
                {'msg': 'login failed',
                 'code': 404,
                 'redirectUrl': fail_redirect_url + 'error=the username or the password error...'})
        login(request, user)
        return http.JsonResponse({'msg': 'login success', 'code': 200, 'redirectUrl': success_redirect_url})
    else:
        to_url = request.GET.get('to')
        error = request.GET.get('error')
        return render(request, 'account/login.html', {
            'error': error,
            'to_url': to_url
        })

def user_logout(request):
    logout(request)
    return redirect(reverse('login'))


def update_user_status(request,  username, status=0):
    if request.method == 'GET':
        # 修改对应用户的管理员账户权限
        # 根据username查找出user
        user = User.objects.filter(username=username).first()
        # 用户存在，根据status修改用户状态
        if user:
            print(status)
            print(user.is_superuser)
            user.is_superuser = True if status == '1' else False
            print(user.is_superuser)
            user.save()

    return redirect(reverse('dashboard_admin'))