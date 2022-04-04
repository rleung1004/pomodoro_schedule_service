import re

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
                return HttpResponse(f'Unauthorized {user_ip}', status=401)
        return response
