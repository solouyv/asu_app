from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.users.models import User, UserRole
from api.subjects.models import Subject
from asu_app.settings import SYSTEM_ADMINISTRATION_SUBJECT_ID
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    is_online = serializers.ReadOnlyField()
    last_seen = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'group',
            'role',
            'is_online',
            'last_seen',
        )


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(
        min_length=8, required=True, write_only=True
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            group=validated_data['group'],
            )
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'group',
            'teacher_subjects',
            'is_superuser',
            'role',
            )


class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(
        min_length=8, required=True, write_only=True
        )
    teacher_subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            )
        user.teacher_subjects.set(validated_data['teacher_subjects'])
        user.user_permissions.add(
                *Permission.objects.filter(codename__iendswith='test').all(),
                *Permission.objects.filter(codename__iendswith='lab').all(),
                *Permission.objects.filter(
                    codename__iendswith='lecture').all(),
                *Permission.objects.filter(codename__iendswith='folder').all(),
                *Permission.objects.filter(codename__iendswith='file').all(),
                *Permission.objects.filter(
                    codename__iendswith='semester').all(),
                *Permission.objects.filter(
                    codename__iendswith='question').all(),
                *Permission.objects.filter(
                    codename__iendswith='answeroption').all(),
                Permission.objects.get(codename='view_testsresult'),
            )
        if (
            SYSTEM_ADMINISTRATION_SUBJECT_ID
            in [subj.id for subj in validated_data['teacher_subjects']]
        ):
            user.user_permissions.add(
                *Permission.objects.filter(
                    codename__iendswith='maincommands').all(),
                *Permission.objects.filter(
                    codename__iendswith='subcommands').all(),
                *Permission.objects.filter(
                    codename__iendswith='devices').all(),
            )
        user.is_staff = True
        user.role = UserRole.TEACHER
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'group',
            'teacher_subjects'
            )
