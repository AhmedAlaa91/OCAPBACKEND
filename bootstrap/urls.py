"""carpooling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.website.api_urls import OpenAPIHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="OCAP APIs",
        default_version="v1",
        description="a web portal for car pooling between orange employees ",
        terms_of_service="https://www.orange-business.com/en",
        contact=openapi.Contact(email="mohamed.g.ismail@orange.com"),
        license=openapi.License(name="[OS] Orange Business License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=OpenAPIHttpAndHttpsSchemaGenerator,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.website.api_urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/v1/",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0,
        ),
        name="schema-swagger-ui",
    ),
    # apps URLs
    path("", include("apps.pages.urls")),
    path("", include("apps.website.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views import defaults as default_views

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    urlpatterns += staticfiles_urlpatterns()
