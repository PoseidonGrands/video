from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse

from app.model.client_user import ClientUser
from app.utils.common import validate_required_fields
from app.utils.consts import COOKIE_NAME


def client_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)

        user = ClientUser.get_user(username, password)
        print(user)
        if user:
            # 设置cookie
            resp = JsonResponse({'code': 200, 'msg': 'success', 'error': ''})
            resp.set_cookie(COOKIE_NAME, str(user.id))
            print('resp', resp)
            return resp
        else:
            return JsonResponse({'code': -1, 'msg': 'failed', 'error': '?error=the username or password error...'})
    else:
        error = request.GET.get('error', '')
        current_url = request.path
        return render(request, 'client/client_login.html', {
            'error': error,
            'token': request.META['CSRF_COOKIE'],
            'current_url': current_url
        })


def client_reg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 字段是否完整
        error = validate_required_fields(username, password)
        if error:
            return JsonResponse({'code': -1, 'msg': 'failed', 'error': error})

        # 用户是否存在
        user = ClientUser.objects.filter(username=username).first()
        if user:
            return JsonResponse({'code': -1, 'msg': 'failed', 'error': '?error=the user is exist...'})

        ClientUser.add(username=username, password=password)
        return JsonResponse({'code': 200, 'msg': 'success', 'error': ''})
    else:
        error = request.GET.get('error', '')
        current_url = request.path
        return render(request, 'client/client_reg.html', {
            'error': error,
            'token': request.META['CSRF_COOKIE'],
            'current_url': current_url
        })


def client_logout(request):
    ret = redirect(reverse('client_login'))
    ret.delete_cookie(COOKIE_NAME)
    return ret
