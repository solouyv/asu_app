import netmiko
from rest_framework import viewsets
from api.console.models import Devices, MainCommands
from api.console.serializers import DeviceSerializer, CommandSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from asu_app.custom_permissions import ReadOnlyIfAllowed, ConsolePermissions
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from asu_app.settings import WEB_GNS_HOST


class Console():
    def __init__(self):
        self.is_connected = False
        self.send_term_length = True

    def connect(self, request, device):
        self.__gns = netmiko.ConnectHandler(
            device_type='generic_termserver_telnet',
            ip=str(device.host),
            username=str(device.username),
            password=str(device.password),
            port=str(device.port)
            )
        self.is_connected = True
        if self.send_term_length:
            self.__gns.send_command("terminal length 0")
            self.send_term_length = False

    def disconnect(self):
        self.__gns.disconnect()
        self.is_connected = False

    def execute_command(self, command):
        if self.is_connected is False:
            return "Connection error"
        # if '?' in command:
        #     return command_info(command)
        result = self.__gns.send_command_timing(command, delay_factor=0)
        prompt = self.__gns.find_prompt()
        return result, prompt


console = Console()


def command_info(command):
    command = command.replace('?', '').replace(' ', '')
    try:
        db_command = MainCommands.objects.get(
            command_name__iexact=command)
    except Exception:
        return 'Command "{}" not found'.format(command)
    result = 'Command: {}\nDescription: {}\n'.format(
        db_command.command_name, db_command.description)
    subcommands = db_command.subcommands.all()
    if subcommands:
        result += 'Subcommands:\n'
        subcommand_result = '\n'.join(
            ['Subcommand: {}\nDescription: {}'.format(
                subcom.subcommand_name, subcom.description)
                for subcom in subcommands])
        return result + subcommand_result
    return result + 'Subcommands not found'


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnlyIfAllowed]
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer


class CommandViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnlyIfAllowed]
    queryset = MainCommands.objects.all()
    serializer_class = CommandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['command_name', 'subcommands__subcommand_name']


class ConnectToDeviceView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | ConsolePermissions]

    def post(self, request, format='json'):
        try:
            device = Devices.objects.get(pk=request.data['id'])
            console.connect(request, device)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DisconnectFromDeviceView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | ConsolePermissions]

    def post(self, request, format='json'):
        try:
            console.disconnect()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ExecuteCommandView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | ConsolePermissions]

    def post(self, request, format='json'):
        try:
            device = Devices.objects.get(pk=request.query_params['id'])
            console.connect(request, device)
            command = request.data["command"]
            result, prompt = console.execute_command(command)
            console.disconnect()
            return Response({"result": result, "prompt": prompt}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WebGNSView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | ConsolePermissions]

    def get(self, request):
        redirect(WEB_GNS_HOST)


def web_gns_view(request):
    return redirect(WEB_GNS_HOST)
