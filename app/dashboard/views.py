from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from ..utils.permission import dashboard_auth


# @login_required(login_url='/account/login?error=you need to login')
@dashboard_auth
def index(request):
    """进入该页面需要校验：1、是否登录 2、用户是否有权限访问"""
    return render(request, 'dashboard/index_base.html')


# @login_required(login_url='/account/login?error=you need to login')
@dashboard_auth
def admin_manager(request,  page_index=None, page_opt=None):
    # 通过参数跳转页面
    index = request.GET.get('page_index')
    if not index:
        # 什么参数都没传
        if not page_index:
            page_index = 1
        page_index = int(page_index)
        # 根据用户点击的上/下一页进行页数修改
        if page_opt == 'next':
            page_index += 1
        elif page_opt == 'prev':
            page_index -= 1
    else:
        page_index = int(index)

    # print('当前页码', page_index)

    # 取出全部用户
    users = User.objects.all()
    # 每页数据
    per_page_count = 2
    p = Paginator(users, per_page_count)
    page = p.page(page_index)

    total_items = page.paginator.count
    total_page = page.paginator.num_pages

    return render(request, 'dashboard/manager_admin.html',
          {
                    'page': page,
                    'total_items': total_items,
                    'total_page': total_page,
                    'page_index': int(page_index)
                    })


# @login_required(login_url='/account/login?error=you need to login')
@dashboard_auth
def admin_user(request):
    return render(request, 'dashboard/manager_user.html')


# @login_required(login_url='/account/login?error=you need to login')
@dashboard_auth
def admin_video(request):
    return render(request, 'dashboard/manager_video.html')



