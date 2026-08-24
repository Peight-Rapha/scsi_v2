class CurrentBrokerageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        request.brokerage = None
        if user and user.is_authenticated:
            request.brokerage = getattr(user, 'brokerage', None)
        return self.get_response(request)
