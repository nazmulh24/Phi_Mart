from django.core.exceptions import ValidationError


def validate_file_size(file):
    """---Validate that the file size is under 5 MB.---"""

    max_size = 5 * 1024 * 1024  # ---> 5 MB
    if file.size > max_size:
        raise ValidationError("File size must be under 5 MB.")
