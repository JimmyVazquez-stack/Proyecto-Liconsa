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


def user_group_processor(request):
    if request.user.is_authenticated:
        es_coordinador = request.user.groups.filter(name__iexact='coordinador').exists()
        es_staff = request.user.is_staff
    else:
        es_coordinador = False
        es_staff = False

    return {
        'es_coordinador': es_coordinador,
        'es_staff': es_staff,
    }