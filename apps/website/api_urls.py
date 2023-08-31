from drf_yasg.generators import OpenAPISchemaGenerator


class OpenAPIHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = (
            ["http"]
            if request.get_host().startswith(
                "127.0.0.1",
            )
            else ["https"]
        )
        return schema


urlpatterns = []
