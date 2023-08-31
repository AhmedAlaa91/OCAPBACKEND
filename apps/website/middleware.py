from django.shortcuts import redirect, render
from django.urls import reverse
import datetime


class UserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # prevent auth user to access register page
            if request.path == reverse('website.register'):
                return redirect('pages.home')

        if request.user.is_authenticated and request.user.profile:
            # show disclaimer page each 6 months
            if datetime.date.today() >= request.user.profile.legal_consent_date:
                if request.path != reverse('website.legalDisclaimer'):
                    return redirect(reverse('website.legalDisclaimer'))

            # prevent auth user to access discaimer page before 6 months
            if request.path == reverse('website.legalDisclaimer') and datetime.date.today() < request.user.profile.legal_consent_date:
                return redirect('pages.home')
            
        response = self.get_response(request)
        return response
