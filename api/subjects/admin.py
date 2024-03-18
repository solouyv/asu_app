from django.contrib import admin
from api.subjects.models import Lab, Subject, Semester, Folder, File, Lecture


class FileInline(admin.StackedInline):
    model = File
    extra = 1


class FolderAdmin(admin.ModelAdmin):
    inlines = [FileInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "semester" and not request.user.is_superuser:
            kwargs["queryset"] = Semester.objects.filter(
                subject__in=request.user.teacher_subjects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FolderInline(admin.StackedInline):
    model = Folder
    extra = 1


class LabInline(admin.StackedInline):
    model = Lab
    extra = 1


class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 1


class SemesterAdmin(admin.ModelAdmin):
    inlines = [FolderInline, LabInline, LectureInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject" and not request.user.is_superuser:
            kwargs["queryset"] = Subject.objects.filter(
                id__in=[subj.id for subj in request.user.teacher_subjects.all()])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LabAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "semester" and not request.user.is_superuser:
            kwargs["queryset"] = Semester.objects.filter(
                subject__in=request.user.teacher_subjects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LectureAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "semester" and not request.user.is_superuser:
            kwargs["queryset"] = Semester.objects.filter(
                subject__in=request.user.teacher_subjects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FileAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "folder" and not request.user.is_superuser:
            kwargs["queryset"] = Folder.objects.filter(
                semester__subject__in=request.user.teacher_subjects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Lab, LabAdmin)
admin.site.register(Subject)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Lecture, LectureAdmin)
