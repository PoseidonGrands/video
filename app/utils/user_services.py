import base64
import hashlib
import string
import random


class UserService(object):
    @staticmethod
    def gene_salt(length=6):
        # string.ascii_letters是a-z，string.digits是0-9
        salt = [random.choice((string.ascii_letters + string.digits)) for _ in range(length)]
        return ''.join(salt)

    @staticmethod
    def gene_pwd(pwd, salt):
        # 把密码转换成字节串再将密码base64加密最后生成md5
        m = hashlib.md5()
        _str = f'{base64.encodebytes(pwd.encode("utf-8"))}-{salt}'
        m.update(_str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def gene_auth(user_info):
        """生成cookie"""
        m = hashlib.md5()
        _str = f'{user_info.id}-{user_info.login_name}-{user_info.login_pwd}'
        m.update(_str.encode('utf-8'))
        return m.hexdigest()
