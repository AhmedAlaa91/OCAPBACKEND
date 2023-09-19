from base64 import b64encode

from rest_framework import serializers
from apps.website.utils.image_resize import get_profile_picture_resized


class ProfilePreview:
    """
    Profile Preview simple model
    """

    def __init__(self, profile_photo):
        self.photo = profile_photo.name
        img, format = get_profile_picture_resized(profile_photo)
        self.photo_resized = b64encode(img.getvalue()).decode("utf-8")
        self.format = format


class ProfilePreviewSerializer(serializers.Serializer):
    profile_photo = serializers.ImageField(required=True, write_only=True)
    photo_resized = serializers.CharField(read_only=True)
