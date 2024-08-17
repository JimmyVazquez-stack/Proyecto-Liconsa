# usuarios/context_processors.py

from django.contrib.auth import get_user_model

def user_context(request):
    user = request.user
    user_info = None
    user_groups = None
    es_coordinador = False
    es_staff = False

    if user.is_authenticated:
        user_info = user
        user_groups = user.groups.all()
        es_coordinador = user.groups.filter(name__iexact='coordinador').exists()
        es_staff = user.is_staff

    return {
        'user_info': user_info,
        'user_groups': user_groups,
        'es_coordinador': es_coordinador,
        'es_staff': es_staff,
    }
