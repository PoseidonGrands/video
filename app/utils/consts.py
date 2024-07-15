import enum
from enum import Enum


COOKIE_NAME = 'django_video_cookie_name'


class VideoType(Enum):
    movie = ('movie', '电影')
    cartoon = ('cartoon', '卡通')
    anime = ('anime', '动漫')
    vlog = ('vlog', 'vlog')
    lubo = ('lubo', '录播')
    other = ('other', '其他')

    @property
    def label(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]


class FromType(Enum):
    youku = ('youku', '优酷')
    tengxun = ('tengxun', '腾讯视频')
    bilibili = ('bilibili', 'b站')
    aqiyi = ('aqiyi', '爱奇艺')
    custom = ('custom', '自制')

    @property
    def label(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]


class NationalityType(Enum):
    china = ('china', '中国')
    korea = ('korea', '韩国')
    american = ('american', '美国')
    japan = ('japan', '日本')
    other = ('other', '其他')

    @property
    def label(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]

class IdentifyType(Enum):
    performer = ('performer', '演员')
    script_writer = ('script_writer', '编剧')
    director = ('director', '导演')

    @property
    def label(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]