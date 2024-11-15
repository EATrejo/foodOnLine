import os
from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] # Ejemplo: cover-image.jpg => Significa que en el index jpg es numero 1. (ext)
    print(ext)
    valid_exptensions = ['.png', '.jpg', 'jpeg']
    if not ext.lower() in valid_exptensions:
        raise ValidationError('Unsupported file extension. Allowed extensions: ' + str(valid_exptensions))