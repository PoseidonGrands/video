import os
import time

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from app.model.video import Video, VideoSub
from app.tasks.task import video_save_task


def enum_type_check(obj, type, msg):
    """检查传入的类型是否存在于指定枚举类型中"""
    try:
        obj[type]
    except:
        return {'code': -1, 'msg': msg}
    return {'code': 1, 'msg': 'success'}


def validate_required_fields(*args):
    """验证是否存在错误"""
    error = ''
    print(args)
    if not all(args):
        error = '?error=missing field...'
    return error


def handle_video(upload_file, video_id, number):
    # 定义输入/输出路径
    file_path_in = os.path.join(settings.MEDIA_ROOT, 'dashboard/temp_in')
    file_path_output = os.path.join(settings.MEDIA_ROOT, 'dashboard/temp_out')

    # 文件名与后缀分开
    file_name_cut = upload_file.name.split('.')
    # 构建输入文件名
    file_name = f'{file_name_cut[0]}_{int(time.time())}.{file_name_cut[1]}'

    # 输入文件的完整路径
    path_name_in = f'{file_path_in}/{file_name}'

    print(file_path_in, file_path_output, file_name)

    # 保存文件
    fs = FileSystemStorage()
    # 保存后的文件名
    filename = fs.save(path_name_in, upload_file).split("/")[-1]
    print('filename', filename)

    path_name_input = f'{file_path_in}/{filename}'
    path_name_output = f'{file_path_output}/{filename}'

    # 对视频进行容器更换（不转码
    command = f'ffmpeg -i {path_name_input} -c copy {path_name_output}'

    # 将自制视频的集数信息保存到数据库
    video = Video.objects.filter(id=video_id).first()
    video_sub_id = VideoSub.objects.create(
        url='',
        name=filename,
        number=number,
        video=video
    )

    print('celery before')
    # celery处理视频转码、上传、数据库保存（celery的任务不要传递对象，可能出问题？
    video_save_task.delay(command, filename, path_name_input, path_name_output, video_sub_id.id)
    print('celery after')


def remove_video_local(videos):
    """将路径的视频全部移除"""
    for video in videos:
        if os.path.exists(video):
            os.remove(video)


