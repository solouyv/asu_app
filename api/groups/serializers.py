from rest_framework import serializers
from api.groups.models import Group, Speciality


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
