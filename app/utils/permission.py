
import functools

from django.shortcuts import redirect, reverse

def dashboard_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        # 没登录或不是超级管理员
        if not user.is_authenticated and not user.is_superuser:
            return redirect(f'{reverse("login")}?to={request.get_full_path()}')
        return func(request, *args, **kwargs)
    return wrapper