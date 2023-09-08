from imagekit import ImageSpec
from imagekit.processors import ResizeToFill


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(380, 380)]
    format = "PNG"
    options = {"quality": 100}


def get_profile_picture_resized(img):
    image_generator = Thumbnail(source=img)
    img_resized = image_generator.generate()
    return (img_resized, image_generator.format)
