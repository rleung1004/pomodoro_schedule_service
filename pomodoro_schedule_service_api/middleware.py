import json
import socket

from django.http import HttpResponse
from pomodoro_schedule_service.settings import ALLOWED_HOST_NAME


class NeedToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "server_fqdn": socket.gethostbyname(socket.getfqdn()),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
        log_data["request_body"] = req_body

        print(log_data)

        socket_host_name = socket.gethostbyname(socket.gethostname())

        for host_name in ALLOWED_HOST_NAME:
            authenticated_by_host = host_name == socket_host_name
            if not authenticated_by_host:
                socket.gethostbyname(socket.gethostname())
                socket.gethostbyname(socket.getfqdn())
                return HttpResponse(f'Unauthorized host:{request.get_host()}', status=401)
        response = self.get_response(request)
        return response
