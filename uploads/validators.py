from django.core.exceptions import ValidationError
import os


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.doc', '.docx']
    if not ext.lower() in valid_extension:
        raise ValidationError(u'Unsupported file extension')
