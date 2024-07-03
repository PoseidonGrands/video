from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django import http
from django.views.decorators.csrf import csrf_exempt

from app.model.video import Video, VideoSub, VideoStar
from app.utils.common import enum_type_check
from app.utils.consts import VideoType, FromType, NationalityType, IdentifyType


@csrf_exempt
def video_external(request):
    if request.method == 'GET':
        error = request.GET.get('error', None)
        # 获取存储的视频信息
        videos = Video.objects.exclude(from_to=FromType.custom)

        return render(request, 'dashboard/video_external.html',
                  {
                      'VideoType': list(VideoType),
                      'FromType': list(FromType)[:-1],
                      'NationalityType': list(NationalityType),
                      'videos': videos,
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


@csrf_exempt
def video_detail(request, video_id=None, current_page=1, page_opt=None):
    if request.method == 'POST':
        ret_obj = {
            'code': 200,
            'msg': 'success',
            'data': {}
        }
        error = ''
        # 获取集数
        try:
            video_url = request.POST.get('video_url')
            video_number = int(request.POST.get('video_number', 1))
            print(video_number)

            # 集数不能小于<1
            if int(video_number) < 1:
                error = '?error=invalid video number'

            # 数据是否确实
            if not all([video_url, video_number]):
                error = '?error=video_url and video_number are required'

            # 存入数据库
            VideoSub.objects.create(url=video_url, video_id=video_id, number=video_number)
        except Exception as e:
            ret_obj = {
                'code': 403,
                'msg': 'failed',
                'error': str(e),
                'data': {}
            }
        if error:
            ret_obj['error'] = error
            ret_obj['code'] = 403
            ret_obj['msg'] = 'failed'
        return http.JsonResponse(ret_obj)
    else:
        error = request.GET.get('error', None)

        video = Video.objects.filter(id=video_id).first()
        video_sub = VideoSub.objects.filter(video=video)
        video_star = VideoStar.objects.filter(video_id=video_id)
        print(video_star)

        # 分页
        current_page = int(current_page)
        if page_opt == 'prev':
            current_page -= 1
        elif page_opt == 'next':
            current_page += 1
        per_page_count = 4
        p = Paginator(video_sub, per_page_count)
        page = p.page(current_page)

        return render(request, 'dashboard/video_detail.html',
                      {
                          'error': error,
                          'video_id': video.id,
                          'video': video,
                          'video_sub': video_sub,
                          'page': page,
                          'current_page': current_page,
                          'total_page': page.paginator.num_pages,
                          'identify_type': list(IdentifyType),
                          'stars': video_star
                      })


@csrf_exempt
def video_detail_performer(request, video_id=None):
    if request.method == 'POST':
        ret_obj = {
            'code': 200,
            'msg': 'success',
            'data': {}
        }
        error = ''
        video_id = request.POST.get('video_id')
        name = request.POST.get('star_name')
        identify = request.POST.get('star_identify')

        if not all([video_id, name, identify]):
            error = '?error=missing field...'

        # 检查类型是否匹配
        if not error:
            print(IdentifyType)
            print(identify)
            identify_check = enum_type_check(IdentifyType, identify, f'the type {identify} is not exist...')

            if identify_check['code'] == -1:
                error = f'?error={identify_check["msg"]}'

        # 没有问题，入库
        if not error:
            try:
                video = Video.objects.filter(id=video_id).first()
                VideoStar.objects.create(video=video, name=name, identify=identify)
            except:
                ret_obj = {
                    'code': 403,
                    'msg': 'failed',
                    'data': {}
                }
        else:
            ret_obj['error'] = error
            ret_obj['code'] = 403
            ret_obj['msg'] = 'failed'

        print(ret_obj)
        return http.JsonResponse(ret_obj)


@csrf_exempt
def video_detail_performer_del(request, video_id=None):
    """演员信息删除"""
    try:
        VideoStar.objects.filter(video_id=video_id).delete()
    except:
        print('del error...')
    return redirect(reverse('video_detail', kwargs={'video_id': video_id}))
