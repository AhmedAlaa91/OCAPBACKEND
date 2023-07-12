import json
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View
from website.forms.register import ChangeUserForm
from website.forms.register import ProfileForm
from website.forms.register import RegisterForm


class AuthView(View):
    context = {}
    def get_area_name(area_id):
        area_name = ""
        current_dir = Path.cwd()
        areas_file_loc = 'static/json/areas.json'
        f = open(current_dir.joinpath(areas_file_loc), encoding='utf8')
        areas = json.load(f)['data']
        for area in areas:
            if area["id"] == area_id:
                area_name = area["city_name_en"]
                return area_name

    def get_city_name(city_id):
        city_name = ""
        current_dir = Path.cwd()
        cities_file_loc = 'static/json/cities.json'
        f = open(current_dir.joinpath(cities_file_loc), encoding='utf8')
        cities = json.load(f)['data']
        for city in cities:
            if city["id"] == city_id:
                city_name = city["governorate_name_en"]
                return city_name

    def get_areas():
        current_dir = Path.cwd()
        areas_file_loc = 'static/json/areas.json'
        f = open(current_dir.joinpath(areas_file_loc), encoding='utf8')
        areas = json.load(f)['data']
        f.close()
        return areas

    def register(request):
        context = {}
        if request.method == 'GET':
            context['user_form'] = RegisterForm(request=request)
            context['profile_form'] = ProfileForm()
            context['context'] = 'create'
            context['areas'] = AuthView.get_areas()
            return render(request, 'register.html', context)

        if request.method == 'POST':
            user_form = RegisterForm(request.POST)
            profile_form = ProfileForm(request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.area = AuthView.get_area_name(request.POST.get('area'))
                profile.city = AuthView.get_city_name(request.POST.get('city'))
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
            context['areas'] = AuthView.get_areas()
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
                profile.area = AuthView.get_area_name(request.POST.get('area'))
                profile.city = AuthView.get_city_name(request.POST.get('city'))
                profile.save()
                messages.success(request, 'Edit profile done successfully.')
                return redirect('/')
            else:
                return render(request, 'register.html', {'user_form': user_form,'profile_form':profile_form})
