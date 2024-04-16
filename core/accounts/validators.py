from django.core.exceptions import ValidationError
import re

def validate_cellphone_number(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError("Phone number must be entered in the format: '09123456789'", code='invalid_phone_number')