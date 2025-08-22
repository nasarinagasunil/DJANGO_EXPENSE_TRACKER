from tracker.models import RequestLogs
class RequestLoggings:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        request_info = request
        RequestLogs.objects.create(
            request_info = vars(request_info),
            request_type = request_info.method,
            request_method = request_info.path
        )
        print(vars(request))
        return response