def user_group_processor(request):
    if request.user.is_authenticated:
        es_coordinador = request.user.groups.filter(name__iexact='coordinador').exists()
    else:
        es_coordinador = False
   

    return {
        'es_coordinador': es_coordinador,
    }