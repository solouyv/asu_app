from datetime import datetime
from django.db import models
from api.subjects.models import Lab, Lecture
from django.conf import settings
from django.shortcuts import reverse


class Test(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название'
        )
    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name='tests',
        null=True,
        blank=True,
        verbose_name='Лабораторная работа'
        )
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='tests',
        null=True,
        blank=True,
        verbose_name='Лекция'
        )
    attempts = models.PositiveIntegerField(verbose_name='Количество попыток')
    timer = models.PositiveIntegerField(
        verbose_name='Ограничение по времени (в минутах)'
        )
    start_date = models.DateTimeField(
        verbose_name='Тест будет доступен со следующей даты',
        blank=True,
        null=True
        )
    end_date = models.DateTimeField(
        verbose_name='Тест будет доступен до следующей даты',
        blank=True,
        null=True
        )
    is_gns3 = models.BooleanField(verbose_name='Выполнять в GNS?', default=False)

    def __str__(self):
        return 'Тест: "{}"'.format(self.name)

    def get_absolute_url_for_lab(self):
        return reverse('test_detail', kwargs={
            'test_id': self.id,
            'lab_id': self.lab.id,
            'subj_id': self.lab.semester.subject.id,
            'sem_id': self.lab.semester.id
            })

    def get_absolute_url_for_lecture(self):
        return reverse('test_detail', kwargs={
            'test_id': self.id,
            'lecture_id': self.lecture.id,
            'subj_id': self.lecture.semester.subject.id,
            'sem_id': self.lecture.semester.id
            })

    def get_report_url(self):
        kwargs = {
            'test_id': self.id,
            }
        if self.lab:
            kwargs.update({
                'lab_id': self.lab.id,
                'subj_id': self.lab.semester.subject.id,
                'sem_id': self.lab.semester.id
                })
        else:
            kwargs.update({
                'lecture_id': self.lecture.id,
                'subj_id': self.lecture.semester.subject.id,
                'sem_id': self.lecture.semester.id
                })
        return reverse('test_report', kwargs=kwargs)

    def get_update_url(self):
        return '/admin/tests/test/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/tests/test/{}/delete/'.format(self.id)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question = models.TextField(max_length=255, verbose_name='Вопрос')
    image = models.ImageField(
        upload_to='question_pictures/',
        blank=True,
        verbose_name='Изображение (опционально)')
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест')
    weight = models.PositiveIntegerField(
        verbose_name='Вес вопроса (Целое положительное число)',
        default=1
    )

    def __str__(self):
        return 'Вопрос к тесту "{}"'.format(self.test.name)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    answer = models.TextField(max_length=255, verbose_name='Вариант ответа')
    is_right = models.BooleanField(verbose_name='Ответ верный?', default=False)
    weight = models.IntegerField(
        verbose_name='Вес ответа (Целое число, для неправильных ответов '
        'используйте отрицательный вес, но для точности результата '
        'соблидайте баланс, сумма весов правильных и '
        'неправильных ответов должна быть равна нулю)',
        default=1
    )

    def __str__(self):
        return 'Вариант ответа к вопросу "{}"'.format(self.question.question)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        unique_together = ('answer', 'question')


class TestsResult(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_results',
        verbose_name='Студент')
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Тест')
    mark = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Оценка')
    completion_date = models.DateTimeField(
        default=datetime.now(),
        verbose_name='Дата завершения')

    def __str__(self):
        return 'Студент "{}" Завершил тест "{}" с оценкой "{}"'.format(
            self.student, self.test.name, self.mark)

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'


class AnswerResult(models.Model):
    test_result = models.ForeignKey(
        TestsResult,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Результат теста')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers_results',
        verbose_name='Вопрос')
    is_right = models.BooleanField(verbose_name='Ответ верный?', default=False)
    is_checked = models.BooleanField(verbose_name='Ответ выбран?', default=False)
    answer_text = models.TextField(max_length=255, verbose_name='Вариант ответа', default='none')

    class Meta:
        verbose_name = 'Результат варианта ответа'
        verbose_name_plural = 'Результат вариантов ответов'
