import json
from .models import AccessLog
from django.utils.deprecation import MiddlewareMixin

class AccessLogMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user if request.user.is_authenticated else None
        path = request.path
        method = request.method
        body = ''

        try:
            body_data = request.body.decode('utf-8')
            body = body_data if len(body_data) < 1000 else body_data[:1000] + '...'
        except:
            pass

        AccessLog.objects.create(
            user=user,
            method=method,
            path=path,
            body=body,
            resource=path
        )
        return None
