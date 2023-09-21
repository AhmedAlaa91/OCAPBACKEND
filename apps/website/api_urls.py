from django.urls import path
from drf_yasg.generators import OpenAPISchemaGenerator
from apps.website.views import get_profile_photo_resized_api


class OpenAPIHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = (
            ["http"]
            if request.get_host().startswith(
                "127.0.0.1",
            )
            or request.get_host().startswith(
                "carpool",
            )
            else ["https"]
        )
        return schema


urlpatterns = [
    path("user/profile/preview", get_profile_photo_resized_api, name="pages.profile_api"),
]
