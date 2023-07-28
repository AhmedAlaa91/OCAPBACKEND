from apps.website.jsonData import JsonData
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View
from apps.website.forms.register import ChangeUserForm
from apps.website.forms.register import ProfileForm
from apps.website.forms.register import RegisterForm


class AuthView(View):
    context = {}

    def register(request):
        context = {}
        if request.method == 'GET':
            context['user_form'] = RegisterForm(request=request)
            context['profile_form'] = ProfileForm()
            context['context'] = 'create'
            context['areas'] = JsonData.get_areas()
            return render(request, 'register.html', context)

        if request.method == 'POST':
            user_form = RegisterForm(request.POST)
            profile_form = ProfileForm(request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.city = JsonData.get_city_name(request.POST.get('city'))
                profile.area = JsonData.get_area_name(request.POST.get('area'))
                profile.save()
                messages.success(request, 'You have registered successfully.')
                login(
                    request, user,
                    backend='django.contrib.auth.backends.ModelBackend',
                )
                return redirect('/')
            else:
                return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

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


class ProfileView(LoginRequiredMixin, View):
    def edit_profile(request):
        context = {}
        if request.method == 'GET':
            context['user_form'] = ChangeUserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            profile_form.user = request.user
            context['profile_form'] = profile_form
            context['context'] = 'edit'
            context['areas'] = JsonData.get_areas()
            context['user_area'] = request.user.profile.area
            context['user_city'] = request.user.profile.city
            return render(request, 'register.html', context)

        if request.method == 'POST':
            user_form = ChangeUserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(
                request.POST, instance=request.user.profile,
            )
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.city = JsonData.get_city_name(request.POST.get('city'))
                profile.area = JsonData.get_area_name(request.POST.get('area'))
                profile.save()
                messages.success(request, 'Edit profile done successfully.')
                return redirect('/')
            else:
                return render(request, 'register.html', {'user_form': user_form,'profile_form':profile_form})
