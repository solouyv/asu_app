# Generated by Django 3.2 on 2021-10-24 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(max_length=255, verbose_name='Вариант ответа')),
                ('is_right', models.BooleanField(default=False, verbose_name='Ответ верный?')),
                ('weight', models.IntegerField(default=1, verbose_name='Вес ответа (Целое число, для неправильных ответов используйте отрицательный вес, но для точности результата соблидайте баланс, сумма весов правильных и неправильных ответов должна быть равна нулю)')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
            },
        ),
        migrations.CreateModel(
            name='AnswerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_right', models.BooleanField(default=False, verbose_name='Ответ верный?')),
                ('is_checked', models.BooleanField(default=False, verbose_name='Ответ выбран?')),
                ('answer_text', models.TextField(default='none', max_length=255, verbose_name='Вариант ответа')),
            ],
            options={
                'verbose_name': 'Результат варианта ответа',
                'verbose_name_plural': 'Результат вариантов ответов',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=255, verbose_name='Вопрос')),
                ('image', models.ImageField(blank=True, upload_to='question_pictures/', verbose_name='Изображение (опционально)')),
                ('weight', models.PositiveIntegerField(default=1, verbose_name='Вес вопроса (Целое положительное число)')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('attempts', models.PositiveIntegerField(verbose_name='Количество попыток')),
                ('timer', models.PositiveIntegerField(verbose_name='Ограничение по времени (в минутах)')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Тест будет доступен со следующей даты')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Тест будет доступен до следующей даты')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='TestsResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Оценка')),
                ('completion_date', models.DateTimeField(default=datetime.datetime(2021, 10, 24, 15, 17, 47, 979744), verbose_name='Дата завершения')),
            ],
            options={
                'verbose_name': 'Результат теста',
                'verbose_name_plural': 'Результаты тестов',
            },
        ),
    ]
