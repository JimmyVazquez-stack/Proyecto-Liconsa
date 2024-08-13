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