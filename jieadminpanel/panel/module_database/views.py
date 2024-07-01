from django.views.generic.base import ContextMixin


class ModuleDatabaseMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'module_database'
        return context
