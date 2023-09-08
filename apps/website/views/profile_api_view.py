from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from apps.website.Serilaizers.profile_photo_preview_serializer import ProfilePreviewSerializer, ProfilePreview
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser


@swagger_auto_schema(methods=["POST"], request_body=ProfilePreviewSerializer)
@api_view(["POST"])
@permission_classes((AllowAny,))
@parser_classes([MultiPartParser])
def get_profile_photo_resized_api(request):
    try:
        profile_photo = request.FILES["profile_picture"]
        photo = ProfilePreview(profile_photo=profile_photo)
        if not photo:
            return Response({"detail": "Invalid Photo"}, status=status.HTTP_501_NOT_IMPLEMENTED)
        profile_serializer = ProfilePreviewSerializer(photo)
        return Response(
            data=profile_serializer.data,
            status=status.HTTP_202_ACCEPTED,
        )
    except Exception as ex:
        return Response({"detail": f"Invalid :{str(ex)}"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
