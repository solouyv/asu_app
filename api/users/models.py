import datetime

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import AbstractUser
from api.groups.models import Group
from api.subjects.models import Subject


class UserRole:
    STUDENT = 1
    TEACHER = 2


class User(AbstractUser):
    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Номер телефона')
    avatar = models.ImageField(
        upload_to='profiles/',
        blank=True,
        verbose_name='Аватар (фото)')
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name='Группа',
        null=True,
        blank=True,
        default=None
        )
    teacher_subjects = models.ManyToManyField(
        Subject,
        related_name='teachers',
        verbose_name='Учебные дисциплины',
        through='UsersSubjects',
        through_fields=('user', 'subject'),
        )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя'
        )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия'
        )
    role = models.IntegerField(
        verbose_name='Роль (1 - студент, 2 - преподаватель)',
        blank=True,
        default=UserRole.STUDENT
        )
    projects = models.JSONField(
        verbose_name='GNS3 Проекты',
        blank=False,
        default=[]
    )

    @property
    def full_name(self):
        return '{} {}'.format(self.last_name, self.first_name)

    @property
    def last_seen(self):
        return cache.get(f'seen_{self.id}')

    @property
    def is_online(self):
        if self.last_seen:
            now = datetime.datetime.now()
            if now > self.last_seen + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UsersSubjects(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None
    )
