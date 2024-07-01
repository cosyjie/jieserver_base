import os
import subprocess
from pathlib import Path
import importlib
from importlib.util import find_spec

from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin, TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView

from appcommon.forms import FormBase
from appcommon.helper import subprocess_run
from .models import AppsInfo
from .forms import DeleteConfirmForm


class AppStoreMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'appstore'
        return context

class AppStoreListView(AppStoreMixin, ListView):
    template_name = 'appstore/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '组件商店'
        return context

    def get_queryset(self):
        if 'type' in self.request.GET:
            if self.request.GET['type'] == 'enabled':
                return AppsInfo.objects.filter(status=2)
            if self.request.GET['type'] == 'disabled':
                return AppsInfo.objects.filter(status=3)
        if 'category' in self.request.GET:
            return AppsInfo.objects.filter(category=self.request.GET.get('category').strip())
        return AppsInfo.objects.all()


class AppDetailView(AppStoreMixin, DetailView):
    model = AppsInfo
    template_name = 'appstore/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '组件详情'
        context['breadcrumb'] = [
            {'title': '组件商店', 'href': reverse_lazy('appstore:list') + "?type=all", 'active': False},
            {'title': '组件详情', 'href': '', 'active': True},

        ]
        print(settings.INSTALL_DIR)
        return context


class AppInstallView(AppStoreMixin, FormView):
    form_class = FormBase
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        app_info = AppsInfo.objects.get(pk=self.kwargs['pk'])
        download_url = app_info.download_url

        file_path = settings.INSTALL_DIR / f'{app_info.name_en}.zip'

        if download_url:
            exec_str = f'cd {settings.INSTALL_DIR} && wget -O {app_info.name_en}.zip {download_url}'
            result = subprocess_run(subprocess, exec_str)
            print(result)

        print(file_path)

        if file_path.exists():
            exec_zip = f'unzip -o {file_path} -d {settings.BASE_DIR}/apps/'
            result = subprocess_run(subprocess, exec_zip)
            print(result)

            exec_zip = f'mv {settings.BASE_DIR}/apps/{app_info.name_en}-main {settings.BASE_DIR}/apps/{app_info.name_en}'
            result = subprocess_run(subprocess, exec_zip)
            print(result)

            if result.returncode == 0:
                if app_info.name_en not in settings.APPS_INSTALLED_LIST:
                    settings.APPS_INSTALLED_LIST.append(app_info.name_en)
                    list_str = '","'.join(settings.APPS_INSTALLED_LIST)
                    content = f'APPS_INSTALLED_LIST=["{list_str}"]'
                    with open(Path.joinpath(settings.BASE_DIR, 'conf', 'apps_installed.py'), 'w', encoding='utf-8') as f:
                        f.write(content)

                if app_info.name_en not in settings.APPS_LIST:
                    settings.APPS_LIST.append(app_info.name_en)
                    w_str = '","'.join(settings.APPS_LIST)
                    w_content = f'APPS_LIST=["{w_str}"]'
                    with open(Path.joinpath(settings.BASE_DIR, 'conf', 'apps_list.py'), 'w', encoding='utf-8') as f:
                        f.write(w_content)
                print('生成迁移')
                result = subprocess_run(subprocess,
                    f'{settings.PYENV_DEFAULT_PYTHON_RUN} {settings.BASE_DIR}/manage.py makemigrations'
                )
                print(result)
                print('开始迁移')
                result = subprocess_run(subprocess,
                    f'{settings.PYENV_DEFAULT_PYTHON_RUN} {settings.BASE_DIR}/manage.py migrate'
                )
                print(result)

                print('执行安装')
                module_name = f'apps.{app_info.name_en}.install'
                if find_spec(module_name):
                    module_views = importlib.import_module(module_name)
                    if callable(getattr(module_views, 'setup')):
                        module_views.setup()

                print('修改状态')
                app_info.status = 2
                app_info.save()
        else:
            messages.warning(self.request, '没有找到安装文件！请下载后放置在 /opt/jieserver/install 目录中! ')
            self.success_url = reverse_lazy('appstore:detail', kwargs={'pk': app_info.pk})
        return super().form_valid(form)


class AppDisabledView(AppStoreMixin, FormView):
    form_class = FormBase
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        app_info = AppsInfo.objects.get(pk=self.kwargs['pk'])
        if app_info.name_en in settings.APPS_LIST:
            settings.APPS_LIST.remove(app_info.name_en)
            w_str = '","'.join(settings.APPS_LIST)
            if len(settings.APPS_LIST):
                w_content = f'APPS_LIST=["{w_str}"]'
            else:
                w_content = f'APPS_LIST=[]'

            with open(Path.joinpath(settings.BASE_DIR, 'conf', 'apps_list.py'), 'w', encoding='utf-8') as f:
                f.write(w_content)

        app_info.status = 3
        app_info.save()

        return super().form_valid(form)


class AppRestoreView(AppStoreMixin, FormView):
    form_class = FormBase
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        app_info = AppsInfo.objects.get(pk=self.kwargs['pk'])
        if app_info.name_en not in settings.APPS_LIST:
            settings.APPS_LIST.append(app_info.name_en)
            w_str = '","'.join(settings.APPS_LIST)
            w_content = f'APPS_LIST=["{w_str}"]'
            with open(Path.joinpath(settings.BASE_DIR, 'conf', 'apps_list.py'), 'w', encoding='utf-8') as f:
                f.write(w_content)
        app_info.status = 2
        app_info.save()

        return super().form_valid(form)


class AppUninstallView(AppStoreMixin, DetailView, FormView):
    model = AppsInfo
    form_class = DeleteConfirmForm
    template_name = 'appstore/confirm_uninstall.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '卸载组件'
        context['breadcrumb'] = [
            {'title': '组件商店', 'href': reverse_lazy('appstore:list') + "?type=all", 'active': False},
            {'title': '组件详情', 'href': reverse_lazy('appstore:detail', kwargs={'pk': self.kwargs['pk']}),
             'active': False},
            {'title': '卸载组件', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        import shutil
        from django.contrib.contenttypes.models import ContentType

        app_info = AppsInfo.objects.get(pk=self.kwargs['pk'])

        module_name = f'apps.{app_info.name_en}.install'
        if find_spec(module_name):
            module_views = importlib.import_module(module_name)
            if callable(getattr(module_views, 'uninstall')):
                module_views.uninstall()

        result = subprocess_run(
            subprocess,
            f'{settings.PYENV_DEFAULT_PYTHON_RUN} {settings.BASE_DIR}/manage.py migrate {app_info.name_en} zero',
        )

        ContentType.objects.filter(app_label=app_info.name_en).delete()

        if app_info.name_en in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.remove(f'apps.{app_info.name_en}')

        if app_info.name_en in settings.APPS_INSTALLED_LIST:
            settings.APPS_INSTALLED_LIST.remove(app_info.name_en)
            w_str = '","'.join(settings.APPS_INSTALLED_LIST)
            if len(settings.APPS_INSTALLED_LIST):
                w_content = f'APPS_INSTALLED_LIST=["{w_str}"]'
            else:
                w_content = f'APPS_INSTALLED_LIST=[]'
            with open(Path.joinpath(settings.BASE_DIR, 'conf', 'apps_installed.py'), 'w', encoding='utf-8') as f:
                f.write(w_content)

        if app_info.name_en in settings.APPS_LIST:
            settings.APPS_LIST.remove(app_info.name_en)
            w_str = '","'.join(settings.APPS_LIST)
            if len(settings.APPS_LIST):
                w_content = f'APPS_LIST=["{w_str}"]'
            else:
                w_content = f'APPS_LIST=[]'
            with open(Path.joinpath(settings.BASE_DIR, 'conf', 'apps_list.py'), 'w', encoding='utf-8') as f:
                f.write(w_content)

        # 执行数据库清理
        result = subprocess_run(
            subprocess,
            f'{settings.PYENV_DEFAULT_PYTHON_RUN} {settings.BASE_DIR}/manage.py makemigrations'
        )
        result = subprocess_run(
            subprocess,
            f'{settings.PYENV_DEFAULT_PYTHON_RUN} {settings.BASE_DIR}/manage.py migrate'
        )
        shutil.rmtree(f'{settings.BASE_DIR}/apps/{app_info.name_en}')

        # 更新数据库状态
        app_info.status = 1
        app_info.save()
        return super().form_valid(form)
