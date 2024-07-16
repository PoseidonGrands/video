from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from app.model.client_user import ClientUser
from app.model.comment import UserComment
from app.model.video import Video
from app.utils.common import validate_required_fields


def comment_commit(request):
    video_id = request.POST.get('video_id')
    user_id = request.POST.get('user_id')
    comment = request.POST.get('comment')

    error = validate_required_fields(video_id, comment)

    print('data', video_id, user_id, comment)
    print('error', error)

    if not error:
        video = Video.objects.filter(id=video_id).first()
        user = ClientUser.objects.filter(id=user_id).first()

        _comment = UserComment.objects.create(content=comment, video=video, user=user)
        # 方案1
        data = vars(_comment)
        data.pop('_state')
        # 方案2（模型中定义函数自定义要返回的值
        # data = _comment.data()

        return JsonResponse({'code': 200, 'msg': 'success', 'data': data})

    return JsonResponse({'code': 200, 'msg': 'success', 'error': error})




