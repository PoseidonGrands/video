from django.db import models

from app.utils.consts import VideoType, FromType, NationalityType, IdentifyType


class Video(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    image = models.CharField(max_length=500, null=True, default='')
    type = models.CharField(max_length=32, default=VideoType.cartoon.value)
    from_to = models.CharField(max_length=32, default=FromType.custom.value)
    nationality = models.CharField(max_length=32, default=NationalityType.china.value)
    info = models.TextField(null=True, blank=True)
    status = models.SmallIntegerField(default=1, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'type', 'from_to', 'nationality')

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='video_sub'
    )
    name = models.CharField(max_length=64, null=True, blank=True)
    url = models.CharField(max_length=500, null=False, blank=False)
    number = models.SmallIntegerField(null=False, blank=False, default='1')

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return f'video: {self.video.name}, number: {self.number}'


class VideoStar(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_star')
    name = models.CharField(max_length=64, null=False, blank=False)
    identify = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        unique_together = ('video', 'name')

    def __str__(self):
        return self.name

    @property
    def identify_label(self):
        try:
            label = IdentifyType[self.identify].label
        except:
            return False
        return label
