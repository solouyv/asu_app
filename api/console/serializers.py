from rest_framework import serializers
from api.console.models import MainCommands, Devices, Subcommands


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = '__all__'


class SubCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcommands
        fields = ('subcommand_name', 'description')


class CommandSerializer(serializers.ModelSerializer):
    subcommands = SubCommandSerializer(many=True, read_only=True)

    class Meta:
        model = MainCommands
        fields = '__all__'
