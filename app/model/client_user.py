from django.db import models

from ..utils.user_services import UserService

class ClientUser(models.Model):
    username = models.CharField(max_length=64, null=False, blank=False, unique=True)
    password = models.CharField(max_length=256, null=False, blank=False)
    salt = models.CharField(max_length=256, null=False, blank=False)
    avatar = models.CharField(max_length=500, null=True, default='')
    gender = models.CharField(max_length=32, null=True, default='')
    birthday = models.DateField(null=True, default=None)
    status = models.SmallIntegerField(default=1, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'username:{self.username}, status:{self.status}'

    @staticmethod
    def add(cls, username, password, salt, avatar, gender, birthday, status):
        salt = UserService.gene_salt()
        return cls.objects.create(
            username=username,
            salt=salt,
            password=UserService.gene_pwd(password, salt),
            avatar=avatar,
            gender=gender,
            birthday=birthday,
            status=status)

    @staticmethod
    def get_user(cls, username, password, salt):
        try:
            user = cls.objects.get(username=username, password=UserService.gene_pwd(password, salt))
            return user
        except:
            return None

    def update_password(self, old_password, salt, new_password):
        """old_password为用户输入的旧密码"""
        token = UserService.gene_pwd(old_password, salt)
        if old_password != self.password:
            return False

        new_salt = UserService.gene_salt()
        self.password = UserService.gene_pwd(new_password, new_salt)
        self.salt = new_salt
        self.save()
        return True

    def update_status(self):
        self.status = not self.status
        self.save()




