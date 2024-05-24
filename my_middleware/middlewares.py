import logging

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        response = self.get_response(request)
        self.logger.info(
            '"{method} {path} {protocol}" {status_code}'.format(
                method=request.method,
                path=request.get_full_path(),
                protocol=request.scheme.upper(),
                status_code=response.status_code,
            )
        )
        return response
