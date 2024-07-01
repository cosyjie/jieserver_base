from django.views.generic.base import ContextMixin


class ModuleSystemMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'module_system'
        return context
