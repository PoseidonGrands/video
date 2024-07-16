from django.db import models
from app.model.video import Video
from app.model.client_user import ClientUser


class UserComment(models.Model):
    content = models.TextField(null=False, blank=False)
    status = models.BooleanField(null=False)

    video = models.ForeignKey(
        Video,
        related_name='comment',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        ClientUser,
        related_name='comment',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def data(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user.id,
            'video_id': self.video.id,
            'username': self.user.username
        }

    def __str__(self):
        return f'{self.video.name}-{self.user.username}:{self.content}'
