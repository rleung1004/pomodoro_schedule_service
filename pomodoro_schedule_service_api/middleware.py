import re
import socket

from django.http import HttpResponse
from pomodoro_schedule_service.settings import ALLOWED_IP_BLOCKS


class NeedToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        user_ip = request.META['REMOTE_ADDR']
        for ip in ALLOWED_IP_BLOCKS:
            authenticated_by_ip = re.compile(ip).match(user_ip)
            if not authenticated_by_ip:
                # one or both the following will work depending on your scenario
                socket.gethostbyname(socket.gethostname())
                socket.gethostbyname(socket.getfqdn())
                return HttpResponse(f'Unauthorized \nhost:{request.get_host()} '
                                    f'\nsocket gethost:{socket.gethostbyname(socket.gethostname())} '
                                    f'\nsocket getfqdn{socket.gethostbyname(socket.getfqdn())}', status=401)
        return response
