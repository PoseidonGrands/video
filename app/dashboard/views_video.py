from django.shortcuts import render, redirect, reverse
from django import http
from django.views.decorators.csrf import csrf_exempt

from app.model.video import Video
from app.utils.common import enum_type_check
from app.utils.consts import VideoType, FromType, NationalityType


@csrf_exempt
def video_external(request):
    if request.method == 'GET':
        error = request.GET.get('error', None)
        return render(request, 'dashboard/video_external.html',
                  {
                      'VideoType': list(VideoType),
                      'FromType': list(FromType),
                      'NationalityType': list(NationalityType),
                      'error': error
                  })
    else:
        # 校验视频信息
        name = request.POST.get('name')
        info = request.POST.get('info')
        image = request.POST.get('image')
        video_type = request.POST.get('videoType')
        from_to = request.POST.get('from')
        nationality = request.POST.get('nationality')

        error = ''
        # 检查是否有字段没输入
        if not all([name, info, image, type, from_to, nationality]):
            error = '?error=missing field...'

        if not error:
            # 检查枚举是否符合类型
            video_check = enum_type_check(VideoType, video_type, f'the type {video_type} is not exist...')
            from_check = enum_type_check(FromType, from_to, f'the type {from_to} is not exist...')
            nationality_check = enum_type_check(NationalityType, nationality, f'the type {nationality} is not exist...')

            if video_check['code'] == -1:
                error = f'?error={video_check["msg"]}'
            if from_check['code'] == -1:
                error = f'?error={from_check["msg"]}'
            if nationality_check['code'] == -1:
                error = f'?error={nationality_check["msg"]}'

        if not error:
            # 存入数据库
            Video.objects.create(
                name=name,
                info=info,
                image=image,
                type=video_type,
                from_to=from_to,
                nationality=nationality
            )

        return http.JsonResponse({
           'code': 200,
           'msg': 'success',
            'redirectUrl': 'http://localhost:8001/dashboard/manage/video_external' + error
        })


def video_custom(request):
    return render(request, 'dashboard/video_custom.html')