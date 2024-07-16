
import functools

from django.shortcuts import redirect, reverse

from app.model.client_user import ClientUser
from app.utils.consts import COOKIE_NAME


def dashboard_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        # 没登录或不是超级管理员
        if not user.is_authenticated and not user.is_superuser:
            return redirect(f'{reverse("login")}?to={request.get_full_path()}')
        return func(request, *args, **kwargs)
    return wrapper


def client_auth(request):
    # 检查cookie是否存在
    cookie = request.COOKIES.get(COOKIE_NAME)
    if not cookie:
        return None

    # 把该cookie对应的用户取出来
    user = ClientUser.objects.filter(pk=cookie).first
    if user:
        return user
    else:
        return None



