from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django import http
from django.views.decorators.csrf import csrf_exempt

from app.model.video import Video, VideoSub, VideoStar
from app.utils.base_qiniu import qiniu
from app.utils.common import enum_type_check, validate_required_fields, handle_video
from app.utils.consts import VideoType, FromType, NationalityType, IdentifyType
from app.utils.permission import dashboard_auth


def save_db(video_data):
    """检验数据正确性后保存到数据库"""
    name = video_data.get('name')
    info = video_data.get('info')
    image = video_data.get('image')
    video_type = video_data.get('videoType')
    from_to = video_data.get('from')
    nationality = video_data.get('nationality')
    # print(name, info, image, video_type, from_to, nationality)

    error = ''
    # 检查是否有字段没输入
    error = validate_required_fields(name, info, image, video_type, from_to, nationality)
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
        return ''
    else:
        return error


@dashboard_auth
def video_edit(request, video_id=None, edit_type=None):
    """视频信息编辑"""
    if request.method == 'GET':
        error = request.GET.get('error')
        video = Video.objects.filter(pk=video_id).first()
        return render(request, 'dashboard/video_edit.html', {
            'video': video,
            'VideoType': list(VideoType),
            'FromType': list(FromType)[:-1],
            'NationalityType': list(NationalityType),
            'editType': edit_type,
            'error': error
        })
    else:
        # 获取表单数据
        video_id = request.POST.get('video_id')
        name = request.POST.get('video_name')
        info = request.POST.get('video_info')
        image = request.POST.get('video_image')
        video_type = request.POST.get('video_type')
        if edit_type == 'custom':
            from_to = 'custom'
        else:
            from_to = request.POST.get('video_from')
        nationality = request.POST.get('video_nationality')

        video = Video.objects.filter(pk=video_id).first()
        # 更新视频
        if video:
            video.name = name
            video.info = info
            video.image = image
            video.type = video_type
            video.from_to = from_to
            video.nationality = nationality
            video.save()

        if edit_type == 'custom':
            return redirect(f'{reverse("video_custom")}?error=')
        else:
            return redirect(f'{reverse("video_external")}?error=')


@csrf_exempt
@dashboard_auth
def video_external(request):
    if request.method == 'GET':
        error = request.GET.get('error', None)
        # 获取存储的视频信息
        videos = Video.objects.exclude(from_to=FromType.custom.name)
        print(videos)

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

        video_data = {
            'name': name,
            'info': info,
            'image': image,
            'videoType': video_type,
            'from': from_to,
            'nationality': nationality,
        }

        error = save_db(video_data)
        if error:
            return http.JsonResponse({
               'code': 200,
               'msg': 'success',
               'redirectUrl': 'http://localhost:8001/dashboard/manage/video_external' + error
            })
        else:
            return http.JsonResponse({
                'code': 404,
                'msg': 'failed',
                'redirectUrl': 'http://localhost:8001/dashboard/manage/video_external' + error
            })


@dashboard_auth
def video_change_status(request, video_id=None):
    video = Video.objects.filter(pk=video_id).first()
    if video:
        video.status = not video.status
        video.save()
    return redirect(reverse('video_external'))


@dashboard_auth
@csrf_exempt
def video_detail(request, video_id=None, current_page=1, page_opt=None, edit_type=None):
    """视频详情页"""
    if request.method == 'POST':
        if edit_type == 'custom':
            video_id = request.POST.get('video-id')
            upload_file = request.FILES.get('video-url')
            number = request.POST.get('video-number')

            # 视频转码并上传七牛云
            url, filename = handle_video(upload_file)
            print('filename', filename)

            if url:
                # 将自制视频的地址和集数信息保存到数据库
                try:
                    video = Video.objects.filter(id=video_id).first()
                    VideoSub.objects.create(
                        url=url,
                        name=filename,
                        number=number,
                        video=video
                    )
                except Exception as e:
                    print(e)

            return redirect(reverse('video_detail', kwargs={'video_id': video_id}))
        # 非自制视频通过ajax提交
        else:
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
                print('url', video_url, type(video_url))

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

        video = Video.objects.filter(id=int(video_id)).first()
        video_sub = VideoSub.objects.filter(video=video)
        video_star = VideoStar.objects.filter(video_id=video_id)

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
                          'stars': video_star,
                          'custom_type': FromType.custom.name,
                          'edit_type': edit_type
                      })


@dashboard_auth
@csrf_exempt
def video_detail_episode_edit(request):
    """集数信息修改"""
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        video_sub_id = request.POST.get('sub_id')
        video_url_edit = request.POST.get('video_url_edit')
        video_number_edit = request.POST.get('video_number_edit')

        sub = VideoSub.objects.filter(pk=video_sub_id).first()
        print('sub', video_sub_id)
        if sub:
            sub.number = video_number_edit
            sub.url = video_url_edit
            sub.save()
        return http.JsonResponse({
            'code': 200,
            'msg': 'success',
            'redirectUrl': f'http://localhost:8001/dashboard/manage/video_detail/{video_id}'
        })


@dashboard_auth
def video_detail_episode_del(request, video_id=None, video_sub_id=None, sub_name=None):
    """删除指定集数"""
    error = ''
    print('sub_name', sub_name)
    try:
        VideoSub.objects.filter(pk=video_sub_id).delete()
    except Exception as e:
        error = 'del failed...'
    format_url = reverse('video_detail', kwargs={'video_id': video_id})

    # 数据库删除记录+七牛云删除文件
    if sub_name:
        qiniu.del_file(sub_name)

    return redirect(f'{format_url}?error={error}')


@dashboard_auth
@csrf_exempt
def video_detail_performer(request, video_id=None):
    """人员信息添加和展示"""
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


@dashboard_auth
@csrf_exempt
def video_detail_performer_del(request, video_id=None):
    """演员信息删除"""
    try:
        VideoStar.objects.filter(video_id=video_id).delete()
    except:
        print('del error...')
    return redirect(reverse('video_detail', kwargs={'video_id': video_id}))


@dashboard_auth
def video_custom(request):
    """自制视频"""
    if request.method == 'GET':
        error = request.GET.get('error', '')
        # 获取存储的自制视频信息
        videos = Video.objects.filter(from_to=FromType.custom.name)

        return render(request, 'dashboard/video_custom.html',
                  {
                      'VideoType': list(VideoType),
                      'FromType': list(FromType)[:-1],
                      'NationalityType': list(NationalityType),
                      'videos': videos,
                      'error': error
                  })
    else:
        name = request.POST.get('name')
        info = request.POST.get('info')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = FromType.custom.name
        nationality = request.POST.get('nationality_type')

        video_data = {
            'name': name,
            'info': info,
            'image': image,
            'videoType': video_type,
            'from': from_to,
            'nationality': nationality,
        }
        error = save_db(video_data)
        return redirect(reverse('video_custom', kwargs={'error': error}))
