import os

from video import celery_app

from app.model.video import VideoSub, Video
from app.utils.base_qiniu import qiniu
from video import celery_app


@celery_app.task
def video_save_task(command, filename, path_name_input, path_name_output, video_sub_id):
    print('command:', command)
    os.system(command)

    print('存储前')
    # 七牛云存储
    url = qiniu.put(filename, path_name_output)
    print('存储后')
    # 删除本地的临时文件
    from app.utils.common import remove_video_local
    remove_video_local([path_name_input, path_name_output])

    if url:
        # 将自制视频的地址保存到数据库
        video_sub = VideoSub.objects.filter(id=video_sub_id).first()
        video_sub.url = url
        video_sub.save()
