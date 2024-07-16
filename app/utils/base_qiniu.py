from qiniu import Auth, put_data, put_file, BucketManager
from django.conf import settings


class QINIU(object):
    def __init__(self, space_name, space_url):
        self.space_name = space_name
        self.space_url = space_url
        # 认证AK与SK获取空间对象
        self.q = Auth(settings.QINIU_AK, settings.QINIU_SK)

    def put(self, name, path):
        """
        将视频上传a
        :param name: 上传后的文件名
        :param path: 需要上传的文件的路径
        :return:
        """
        # 获取上传令牌（用某名字上传到某个空间地址是否可行
        token = self.q.upload_token(self.space_name, name)
        # 通过令牌上传文件
        ret, info = put_file(token, name, path)

        if 'key' in ret:
            print(ret)
            print('key是：', ret["key"])
            ret_url = f'{self.space_url}/{ret["key"]}'
            return ret_url
        else:
            print('the key do not exist...')
            return ''

    def del_file(self, name):
        bucket = BucketManager(self.q)
        bucket_name = self.space_name
        key = name
        # 删除bucket_name 中的文件 key
        ret, info = bucket.delete(bucket_name, key)
        print(ret)
        print(info)


qiniu = QINIU(settings.QINIU_SPACE, settings.QINIU_SPACE_URL)
