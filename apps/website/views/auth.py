from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect


class AuthView():
    def login(request):
        """Implement customized django auth backend with Orange Auth. You can refer to AUTHENTICATION_BACKENDS in django settings.

        Parameters
        ----------
        request : HttpRequest
            The request object
        """
        return authenticate(request)

    def logout(request):
        """Logout a user from request sessions.

        Parameters
        ----------
        request : HttpRequest
            The request object
        """
        logout(request=request)
        return redirect(request.META.get('HTTP_REFERER', 'pages.home'))