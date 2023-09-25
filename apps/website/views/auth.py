from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from apps.website.utils.image_resize import get_profile_picture_resized
from apps.website.forms.register import ChangeUserForm, ProfileForm, RegisterForm
from apps.website.jsonData import JsonData
from apps.website.utils.image_resize import Thumbnail
from lib.s3_storage.s3_helpers import create_s3_client
from lib.utils import get_filename_without_ext


class AuthView(View):
    context = {}

    @staticmethod
    def legalDisclaimer(request):
        if request.method == "GET":
            return render(request, "legal_disclaimer.html")

        if request.method == "POST":
            if request.user.is_authenticated and request.user.profile:
                request.user.profile.legal_consent_date = datetime.now() + timedelta(days=180)
                request.user.profile.save()
                return redirect("/")

            return redirect("/register")

    @staticmethod
    def register(request):
        context = dict()
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
                try:
                    # Get img from register form and create s3 client to upload
                    if "profile_picture" in request.FILES.keys():
                        img = request.FILES.get("profile_picture")
                        client, session = create_s3_client()
                        if profile.profile_pic is not None:
                            # delete an image before upload new one
                            client.delete_object(
                                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                Key=f"{settings.AWS_S3_PREFIX}/{profile.profile_pic}",
                            )
                        img_resized, format_type = get_profile_picture_resized(img)
                        file_name = get_filename_without_ext(img.name)
                        client.upload_fileobj(
                            img_resized,
                            settings.AWS_STORAGE_BUCKET_NAME,
                            f"{settings.AWS_S3_PREFIX}/{request.user.username}_{file_name}.{format_type.lower()}",
                        )
                        img.close()
                        profile.profile_pic = f"{request.user.username}_{file_name}.{format_type.lower()}"
                    profile.save()
                    messages.success(request, "You have registered successfully.")
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    return redirect("pages.home")
                except Exception as ex:
                    messages.error(request, f"error : {str(ex)}")
                    return redirect("website.login")
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

    @staticmethod
    def login(request):
        """Implement customized django auth backend with Orange Auth. You can refer to AUTHENTICATION_BACKENDS in django settings.

        Parameters
        ----------
        request : HttpRequest
            The request object
        """
        return authenticate(request)

    @staticmethod
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
    @staticmethod
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
                try:
                    # Get img from register form and create s3 client to upload
                    if "profile_picture" in request.FILES.keys():
                        img = request.FILES.get("profile_picture")
                        client, session = create_s3_client()
                        if profile.profile_pic is not None:
                            # delete an image before upload new one
                            client.delete_object(
                                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                Key=f"{settings.AWS_S3_PREFIX}/{profile.profile_pic}",
                            )
                        img_resized, format_type = get_profile_picture_resized(img)
                        file_name = get_filename_without_ext(img.name)
                        client.upload_fileobj(
                            img_resized,
                            settings.AWS_STORAGE_BUCKET_NAME,
                            f"{settings.AWS_S3_PREFIX}/{request.user.username}_{file_name}.{format_type.lower()}",
                        )
                        img.close()
                        profile.profile_pic = f"{request.user.username}_{file_name}.{format_type.lower()}"

                    profile.save()
                    messages.success(request, "Edit profile done successfully.")
                    return redirect("pages.home")
                except Exception as ex:
                    messages.error(request, f"error : {str(ex)}")
                    return redirect("pages.home")
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
