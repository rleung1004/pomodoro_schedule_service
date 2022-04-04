import json
import socket

from django.http import HttpResponse
from pomodoro_schedule_service.settings import ALLOWED_IP_BLOCKS


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
        user_ip = request.META['REMOTE_ADDR']
        socket_host_name = socket.gethostbyname(socket.gethostname())
        socket_host_fqdn = socket.getfqdn()

        for ip in ALLOWED_IP_BLOCKS:
            authenticated_by_ip = ip == user_ip or\
                                  ip == socket_host_name or\
                                  ip == socket_host_fqdn
            if not authenticated_by_ip:
                # one or both the following will work depending on your scenario
                socket.gethostbyname(socket.gethostname())
                socket.gethostbyname(socket.getfqdn())
                return HttpResponse(f'Unauthorized host:{request.get_host()}', status=401)
        response = self.get_response(request)
        return response
