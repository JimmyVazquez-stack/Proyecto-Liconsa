# usuarios/context_processors.py

from django.contrib.auth import get_user_model

User = get_user_model()

def user_context(request):
    user_info = None
    user_groups = None
    if request.user.is_authenticated:
        try:
            user_info = User.objects.get(username=request.user.username)
            user_groups = user_info.groups.all()
        except User.DoesNotExist:
            pass
    return {
        'user_info': user_info,
        'user_groups': user_groups,
    }