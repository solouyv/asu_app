from datetime import datetime

import pytz
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.simple_tests.models import Test, TestsResult, AnswerResult
from api.simple_tests.serializers import (
    TestSerializer,
    TestDetailSerializer,
    TestResultSerializer,
    TestResultDetailSerializer,
)
from api.users.models import UserRole
from asu_app.custom_permissions import ReadOnly
from asu_app.settings import WEB_GNS_HOST


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Test.objects.all().distinct()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lab', 'lecture']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestDetailSerializer
        return self.serializer_class

    def retrieve(self, request, pk=None):
        test = Test.objects.prefetch_related('questions__answers').get(pk=pk)
        serializer = TestDetailSerializer(test)
        now = datetime.now().replace(tzinfo=pytz.UTC)
        start_date = test.start_date.replace(tzinfo=pytz.UTC)
        end_date = test.end_date.replace(tzinfo=pytz.UTC)
        if start_date > now or end_date < now:
            return Response(
                {'message': 'В данный момент тест недоступен.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        test_results = TestsResult.objects.filter(test=test).filter(
            student=request.user)
        if len(test_results) == int(test.attempts):
            return Response(
                {'message': 'Вы потратили все попытки на выполнение этого теста.'},  # noqa
                status=status.HTTP_400_BAD_REQUEST
            )

        # if test.is_gns3:
        #     return HttpResponseRedirect(WEB_GNS_HOST)

        test_time_key = 'timer_test_{}_{}'.format(test.id, request.user.id)
        test_date_key = 'date_test_{}_{}'.format(test.id, request.user.id)
        if not cache.get(test_time_key):
            cache.set(test_time_key, test.timer * 60, test.timer * 60 * 2)
            cache.set(test_date_key, datetime.now().timestamp(), test.timer * 60 * 2)  # noqa
        estimated_time = int(cache.get(test_time_key) - (
                datetime.now().timestamp() - cache.get(test_date_key)))
        data = {'estimated_time': estimated_time}
        data.update(serializer.data)
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        test = Test.objects.prefetch_related('questions__answers').get(pk=pk)
        test_time_key = 'timer_test_{}_{}'.format(test.id, request.user.id)
        test_date_key = 'date_test_{}_{}'.format(test.id, request.user.id)
        cache.delete(test_time_key)
        cache.delete(test_date_key)
        max_weight = 0
        result_weight = 0
        answers_results = []
        for question in test.questions.all():
            max_weight += question.weight
            answers = set(request.data.get(
                'question_{}'.format(question.id)))
            if not answers:
                continue
            answers_max_weight = 0
            answers_result_weight = 0
            for answer in question.answers.all():
                if answer.is_right:
                    answers_max_weight += answer.weight
                if answer.is_right and answer.answer in answers:
                    answers_result_weight += answer.weight
                if not answer.is_right and answer.answer in answers:
                    answers_result_weight += answer.weight
                answers_results.append(AnswerResult(
                    question=question,
                    is_right=answer.is_right,
                    is_checked=answer.answer in answers,
                    answer_text=answer.answer,
                ))
            if answers_result_weight < 0:
                answers_result_weight = 0
            result_weight += question.weight * (answers_result_weight / answers_max_weight)  # noqa
        if max_weight:
            result_mark = round((result_weight / max_weight) * 10, 2)
        result = TestsResult.objects.create(
            student=request.user,
            test=test,
            mark=result_mark if max_weight else 0
        )
        for answer_result in answers_results:
            answer_result.test_result = result
            answer_result.save()
        serializer = TestResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Test.objects.all().distinct()
        if self.request.user.role == UserRole.STUDENT:
            return (
                Test.objects
                .filter(
                    Q(lab__semester__subject__allowed_specialities__groups__in=[self.request.user.group]) |  # noqa
                    Q(lecture__semester__subject__allowed_specialities__groups__in=[self.request.user.group])  # noqa
                )
                .all().prefetch_related(
                    'lab__semester__subject__allowed_specialities__groups',
                    'lecture__semester__subject__allowed_specialities__groups'
                ).distinct()
            )
        else:
            return (
                Test.objects
                .filter(
                    Q(lab__semester__subject__in=self.request.user.teacher_subjects.all()) |  # noqa
                    Q(lecture__semester__subject__in=self.request.user.teacher_subjects.all())  # noqa
                )
                .all().prefetch_related(
                    'lab__semester__subject',
                    'lecture__semester__subject'
                ).distinct()
            )


class TestResultViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = TestsResult.objects.all().select_related('student__group', 'test')
    serializer_class = TestResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'student__group', 'test']

    def retrieve(self, request, pk=None):
        result = (
            TestsResult.objects
            .prefetch_related('student', 'test__questions__answers_results')
            .get(pk=pk)
        )
        for question in result.test.questions.all():
            question.answers_res = question.answers_results.filter(test_result__id=pk).all()
        serializer = TestResultDetailSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TestsResult.objects.all().select_related('student__group', 'test')
        if self.request.user.role == UserRole.TEACHER:
            return (
                TestsResult.objects
                .filter(
                    Q(test__lab__semester__subject__in=self.request.user.teacher_subjects.all()) |
                    Q(test__lecture__semester__subject__in=self.request.user.teacher_subjects.all())
                )
                .all().select_related('student__group', 'test').distinct()
            )
        else:
            return (
                TestsResult.objects
                .filter(student=self.request.user)
                .all().select_related('student__group', 'test').distinct()
            )
