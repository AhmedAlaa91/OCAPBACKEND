from django.shortcuts import redirect
from django.urls import reverse


class UserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == reverse("website.register"):
                return redirect("pages.home")
        response = self.get_response(request)
        return response
