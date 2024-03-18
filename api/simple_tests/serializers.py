from rest_framework import serializers
from api.simple_tests.models import Test, Question, AnswerOption, TestsResult, AnswerResult


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('answer', 'id')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerOptionSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('question', 'image', 'answers', 'id')


class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Test
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='test.name', read_only=True)
    student = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = TestsResult
        fields = ['id', 'mark', 'completion_date', 'test', 'student', 'name', 'student', 'group'] # noqa

    @staticmethod
    def get_student(instance):
        return f'{instance.student.last_name} {instance.student.first_name}'

    @staticmethod
    def get_group(instance):
        if getattr(instance.student, 'group'):
            return instance.student.group.name


class AnswerResultSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(read_only=True, source="answer_text")

    class Meta:
        model = AnswerResult
        fields = ('is_right', 'is_checked', 'answer', 'id')


class QuestionResultSerializer(serializers.ModelSerializer):
    answers_res = AnswerResultSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('question', 'image', 'answers_res', 'id')


class TestForResultSerializer(serializers.ModelSerializer):
    questions = QuestionResultSerializer(read_only=True, many=True)

    class Meta:
        model = Test
        fields = '__all__'


class TestResultDetailSerializer(serializers.ModelSerializer):
    test = TestForResultSerializer()

    class Meta:
        model = TestsResult
        fields = '__all__'
