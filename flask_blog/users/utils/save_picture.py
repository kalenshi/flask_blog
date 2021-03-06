import os
import secrets
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

image_dir = os.path.join(BASE_DIR, "static", "images")
picture_dimensions = (125, 125)


def save_picture(form_picture):
    """
    Utility to save users profile pictures
    reduced in size.
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    profile_filename = random_hex + file_ext
    picture_path = os.path.join(image_dir, profile_filename)

    with Image.open(form_picture) as i:
        i.thumbnail(picture_dimensions)
        i.save(picture_path)
    return profile_filename
