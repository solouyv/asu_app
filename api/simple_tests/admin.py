from django.contrib import admin
from api.simple_tests.models import Test, TestsResult, Question, AnswerOption
from api.subjects.models import Lab, Lecture
import nested_admin


class AnswerOptionInline(nested_admin.NestedStackedInline):
    model = AnswerOption
    extra = 2


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerOptionInline]


class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lab" and not request.user.is_superuser:
            kwargs["queryset"] = Lab.objects.filter(
                semester__subject__in=request.user.teacher_subjects.all())
        if db_field.name == "lecture" and not request.user.is_superuser:
            kwargs["queryset"] = Lecture.objects.filter(
                semester__subject__in=request.user.teacher_subjects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Test, TestAdmin)
admin.site.register(TestsResult)
admin.site.register(Question)
