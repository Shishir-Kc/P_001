import string
from django.utils.crypto import get_random_string

def generate_unique_code(length=8):
    from .models import Student_info 
    chars = string.ascii_uppercase + string.digits
    while True:
        code = get_random_string(length, allowed_chars=chars)
        if not Student_info.objects.filter(student_code=code).exists():
            return code
