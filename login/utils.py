from django.contrib.auth.models import User



def does_user_exists(email):
    try:
        user = User.objects.filter(email=email).exists()
        if user:
            return True
        else:
            return False
    except User.DoesNotExist:
        return False
    