import json
import socket

from django.http import HttpResponse
from pomodoro_schedule_service.settings import ALLOWED_IP_NAME


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
            "ip": get_client_ip(request)
        }

        req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
        log_data["request_body"] = req_body

        print(log_data)

        socket_fqdn = socket.gethostbyname(socket.getfqdn())

        for ip in ALLOWED_IP_NAME:
            authenticated_by_host = (ip == get_client_ip(request))
            if authenticated_by_host:
                response = self.get_response(request)
                return response

        return HttpResponse(f'Unauthorized ip:{get_client_ip(request)}', status=401)
