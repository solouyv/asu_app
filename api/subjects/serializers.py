import os

from rest_framework import serializers
from api.subjects.models import Lab, Lecture, Folder, File, Subject, Semester
from api.groups.serializers import SpecialitySerializer


class SubjectSerializer(serializers.ModelSerializer):
    allowed_specialities = SpecialitySerializer(read_only=True, many=True)
    allow_console = serializers.ReadOnlyField()

    class Meta:
        model = Subject
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Semester
        fields = '__all__'


class LabSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = '__all__'

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            file_url = obj.file.url
            if request:
                file_url = request.build_absolute_uri(file_url)
            file_url = file_url.replace(
                'http://localhost',
                os.getenv('API_BASE_URL'),
            )
            return file_url
        return None


class LectureSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = '__all__'

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            file_url = obj.file.url
            if request:
                file_url = request.build_absolute_uri(file_url)
            file_url = file_url.replace(
                'http://localhost',
                os.getenv('API_BASE_URL'),
            )
            return file_url
        return None

class FolderSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    folder = FolderSerializer(read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = '__all__'

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            file_url = obj.file.url
            if request:
                file_url = request.build_absolute_uri(file_url)
            file_url = file_url.replace(
                'http://localhost',
                os.getenv('API_BASE_URL'),
            )
            return file_url
        return None
