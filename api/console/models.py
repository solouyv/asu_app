from django.db import models
from django.shortcuts import reverse


class MainCommands(models.Model):
    command_name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Команда')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return 'Команда "{}"'.format(self.command_name)

    def get_absolute_url(self):
        return reverse('command_detail', kwargs={'com_id': self.id})

    def get_update_url(self):
        return '/admin/console/maincommands/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/console/maincommands/{}/delete/'.format(self.id)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Subcommands(models.Model):
    command_id = models.ForeignKey(
        MainCommands,
        on_delete=models.CASCADE,
        verbose_name='Название',
        related_name='subcommands')
    subcommand_name = models.CharField(
        max_length=150, verbose_name='Подкоманда')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return 'Подкоманда "{}" к {}'.format(
            self.subcommand_name, self.command_id)

    class Meta:
        verbose_name = 'Подкоманда'
        verbose_name_plural = 'Подкоманды'


class Devices(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Название устройства',
        unique=True)
    host = models.CharField(max_length=50, verbose_name='Хост')
    port = models.CharField(
        max_length=20,
        default="",
        verbose_name='Порт',
        unique=True)
    username = models.CharField(
        max_length=150, default="", verbose_name='Имя пользователя')
    password = models.CharField(max_length=150, verbose_name='Пароль')

    def __str__(self):
        return 'Устройство "{}" на {}:{}'.format(
            self.name, self.host, self.port)

    def get_absolute_url(self):
        return reverse('device_detail', kwargs={'dev_id': self.id})

    def get_update_url(self):
        return '/admin/console/devices/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/console/devices/{}/delete/'.format(self.id)

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
