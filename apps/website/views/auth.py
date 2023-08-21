from django.conf import settings

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
from django.core.files.base import ContentFile

from lib.s3_storage.s3_helpers import create_s3_client


class AuthView(View):
    context = {}

    def register(request):
        context = {}
        context["areas"] = JsonData.get_areas()
        context["cities"] = JsonData.get_cities_json()
        context["context"] = "create"
        if request.method == "GET":
            context["user_form"] = RegisterForm(request=request)
            context["profile_form"] = ProfileForm()
            return render(request, "register.html", context)

        if request.method == "POST":
            user_form = RegisterForm(request.POST)
            profile_form = ProfileForm(request.POST, request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.city = JsonData.get_city_name(request.POST.get("city"))
                profile.area = JsonData.get_area_name(request.POST.get("area"))
                # # Get img from register form and create s3 client to upload img
                # img = profile_form.cleaned_data.get("profile_picture")
                # client, session = create_s3_client()
                # client.upload_fileobj(
                #     img.open(mode="rb"),
                #     settings.AWS_STORAGE_BUCKET_NAME,
                #     img.name,
                # )
                # img.close()
                # profile.profile_pic = img.name
                profile.save()
                messages.success(request, "You have registered successfully.")
                login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                return redirect("/")
            else:
                return render(
                    request,
                    "register.html",
                    {
                        "user_form": user_form,
                        "profile_form": profile_form,
                        "areas": context["areas"],
                        "cities": context["cities"],
                        "context": context["context"],
                    },
                )

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
        return redirect(request.META.get("HTTP_REFERER", "pages.home"))


class ProfileView(LoginRequiredMixin, View):
    def edit_profile(request):
        context = {}
        context["context"] = "edit"
        context["areas"] = JsonData.get_areas()
        context["cities"] = JsonData.get_cities_json()
        context["user_area"] = request.user.profile.area
        context["user_city"] = request.user.profile.city
        if request.method == "GET":
            context["user_form"] = ChangeUserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            profile_form.user = request.user
            context["profile_form"] = profile_form
            return render(request, "register.html", context)

        if request.method == "POST":
            user_form = ChangeUserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(
                request.POST,
                instance=request.user.profile,
            )
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.city = JsonData.get_city_name(request.POST.get("city"))
                profile.area = JsonData.get_area_name(request.POST.get("area"))
                profile.save()
                messages.success(request, "Edit profile done successfully.")
                return redirect("/")
            else:
                return render(
                    request,
                    "register.html",
                    {
                        "user_form": user_form,
                        "profile_form": profile_form,
                        "areas": context["areas"],
                        "cities": context["cities"],
                        "context": context["context"],
                        "user_city": context["user_city"],
                        "user_area": context["user_area"],
                    },
                )
