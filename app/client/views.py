from django import http
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import *
from django.contrib.auth import *

from app.model.video import Video, VideoSub, VideoStar
from app.utils.consts import FromType
from app.utils.permission import client_auth


def index(request):
    return redirect(reverse('client_external_video'))


def client_external_video(request):
    video = Video.objects.exclude(from_to=FromType.custom.name)
    return render(request, 'client/video.html',
                  {
                      'videos': video
                  })


def client_custom_video(request):
    video = Video.objects.filter(from_to=FromType.custom.name)
    print('video', video)
    return render(request, 'client/video.html',
                  {
                      'videos': video
                  })


def client_video_detail(request, video_id):
    video = Video.objects.filter(id=video_id).first()
    video_sub = VideoSub.objects.filter(video_id=video_id)
    video_star = VideoStar.objects.filter(video_id=video_id)
    return render(request, 'client/video_detail.html', {
        'video': video,
        'video_sub': video_sub,
        'video_star': video_star
    })


def mine(request):
    if request.method == 'GET':
        # 检查是否登录（cookie是否存在
        user = client_auth(request)
        if user:
            return render(request, 'client/mine.html', {
                'user': user
            })
        else:
            # 进入登录页面
            print('未登录')
            return redirect(reverse('client_login'))



