from django.db import models
from django.shortcuts import reverse
from api.groups.models import Speciality
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name='Название')
    allowed_specialities = models.ManyToManyField(
        Speciality,
        related_name='allowed_subjects',
        verbose_name='Специальности, которым доступна данная дисциплина'
        )

    @property
    def allow_console(self):
        return True if self.id == settings.SYSTEM_ADMINISTRATION_SUBJECT_ID else False

    def __str__(self):
        return 'Предмет: "{}"'.format(self.name)

    class Meta:
        verbose_name = 'Предмет (учебная дисциплина)'
        verbose_name_plural = 'Предметы (учебные дисциплины)'


class Semester(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='semesters',
        verbose_name='Предмет')

    def get_absolute_url(self):
        return reverse('folders', kwargs={
            'subj_id': self.subject.id,
            'sem_id': self.id})

    def get_labs_url(self):
        return reverse('labs', kwargs={
            'subj_id': self.subject.id,
            'sem_id': self.id})

    def get_lectures_url(self):
        return reverse('lectures', kwargs={
            'subj_id': self.subject.id,
            'sem_id': self.id})

    def get_update_url(self):
        return '/admin/labs/semester/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/labs/semester/{}/delete/'.format(self.id)

    def __str__(self):
        return 'Семестр: "{}", {}'.format(self.name, self.subject)

    class Meta:
        verbose_name = 'Семестр'
        verbose_name_plural = 'Семестры'


class Lab(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='labs',
        verbose_name='Семестр')
    file = models.FileField(upload_to='labs/', verbose_name='Файл(лаба)')

    def get_absolute_url(self):
        return reverse('lab_detail', kwargs={
            'subj_id': self.semester.subject.id,
            'sem_id': self.semester.id,
            'lab_id': self.id})

    def get_lab_tests_url(self):
        return reverse('tests_list', kwargs={
            'subj_id': self.semester.subject.id,
            'sem_id': self.semester.id,
            'lab_id': self.id})

    def get_update_url(self):
        return '/admin/labs/lab/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/labs/lab/{}/delete/'.format(self.id)

    def __str__(self):
        return 'Лаба "{}", {}'.format(self.name, self.semester)

    class Meta:
        verbose_name = 'Лабораторная работа'
        verbose_name_plural = 'Лабораторные работы'


class Lecture(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name='Семестр')
    file = models.FileField(upload_to='lectures/', verbose_name='Файл(лекция)')

    def get_absolute_url(self):
        return reverse('lecture_detail', kwargs={
            'subj_id': self.semester.subject.id,
            'sem_id': self.semester.id,
            'lecture_id': self.id})

    def get_lecture_tests_url(self):
        return reverse('tests_list', kwargs={
            'subj_id': self.semester.subject.id,
            'sem_id': self.semester.id,
            'lecture_id': self.id})

    def get_update_url(self):
        return '/admin/labs/lecture/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/labs/lecture/{}/delete/'.format(self.id)

    def __str__(self):
        return 'Лекция "{}", {}'.format(self.name, self.semester)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Folder(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='folders',
        verbose_name='Семестр')

    def get_absolute_url(self):
        return reverse('folder_detail', kwargs={
            'subj_id': self.semester.subject.id,
            'sem_id': self.semester.id,
            'folder_id': self.id})

    def get_update_url(self):
        return '/admin/labs/folder/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/labs/folder/{}/delete/'.format(self.id)

    def __str__(self):
        return 'Папка "{}", {}'.format(self.name, self.semester)

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'


class File(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Папка')
    file = models.FileField(
        upload_to='additional_files/',
        verbose_name='Файл'
        )

    def __str__(self):
        return 'Файл "{}", {}'.format(self.name, self.folder)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
