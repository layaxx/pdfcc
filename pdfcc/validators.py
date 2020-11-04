from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if not value.name.endswith('.pdf'):
        raise ValidationError('The File must be a PDF')
    if filesize > 26214400:
        raise ValidationError(
            'The maximum file size that can be uploaded is 25MB')
    else:
        return value
