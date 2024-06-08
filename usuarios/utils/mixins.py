from django.contrib.auth.mixins import UserPassesTestMixin

class GroupRequiredMixin(UserPassesTestMixin):
    group_names = []

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_superuser or user.groups.filter(name__in=self.group_names).exists()
        )

    def handle_no_permission(self):
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(self.request.get_full_path())
'''
Este mixin se encarga de verificar si el usuario pertenece a un grupo en específico.

'''