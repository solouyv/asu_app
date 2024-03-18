from django.db import models
from django.shortcuts import reverse


class Group(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    speciality = models.ForeignKey(
        'Speciality',
        on_delete=models.SET_NULL,
        null=True,
        related_name='groups',
        verbose_name='Специальность')

    def get_report_url(self):
        return reverse('group_report', kwargs={'group_id': self.id})

    def __str__(self):
        return 'Группа "{}"'.format(self.name)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Speciality(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return 'Специальность "{}"'.format(self.name)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
