from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm


class PanelLoginView(LoginView):
    """登录"""
    form_class = LoginForm
    template_name = 'systemauth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '登录'
        return context


class PanelLogoutView(LogoutView):
    """注销登录"""
    pass
