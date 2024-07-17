import socket
import os
import importlib
from pathlib import Path

from django.conf import settings
from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag
def get_hostname():
    return socket.gethostname()


@register.simple_tag
def navbar(parent_menu, submenu):
    # 顶端菜单
    pass


@register.simple_tag
def user_menu(parent_menu, submenu):
    # 用户菜单
    pass


@register.simple_tag
def main_sidebar(parent_menu, current_menu):
    from app_files.conf.apps_enabled import APPS_LIST

    # 左侧主菜单
    menus = {}
    html = ''
    modules_root = Path.joinpath(Path.joinpath(settings.BASE_DIR, 'panel'))

    for module_dir in modules_root.iterdir():
        if module_dir.is_dir() and module_dir.name[:7] == 'module_' and module_dir.name != '__pycache__':
            import_module = importlib.import_module(f'panel.{module_dir.name}.menu')
            module_menu = import_module.menu

            for module_name, module_content in module_menu.items():
                if module_content['position'] == 'main_sidebar':
                    menus[module_name] = module_content

    for app_name in APPS_LIST:
        if os.path.exists(Path.joinpath(settings.APPS_ROOT, app_name, 'menu.py')):
            import_app = importlib.import_module(f'apps.{app_name}.menu')
            app_menu = import_app.menu
            for k, v in app_menu.items():
                if k not in menus:
                    if v['position'] == 'main_sidebar':
                        menus[k] = v

    for app_name in APPS_LIST:
        if os.path.exists(Path.joinpath(settings.APPS_ROOT, app_name, 'menu.py')):
            import_app = importlib.import_module(f'apps.{app_name}.menu')
            app_menu = import_app.menu
            for k, v in app_menu.items():
                if k in menus:
                    if v['child']:
                        for child in v['child']:
                            if child not in menus[k]['child']:
                                menus[k]['child'].append(child)

    for k, value in menus.items():
        if len(value['child']):
            html += '<li class="nav-item'
            if parent_menu == k:
                html += ' menu-open'
            html += '"><a href="#" class="nav-link'
            if parent_menu == k:
                html += ' active'
            html += '"><i class="nav-icon ' + value['ico'] + '"></i><p>' + value['title'] + \
                    '<i class="right fas fa-angle-left"></i></p></a>'

            if value['child']:
                html += '<ul class="nav nav-treeview">'
                for sub in value['child']:
                    html += '<li class="nav-item"><a href="' + sub['href'] + '" class="nav-link'
                    if parent_menu == k and current_menu == sub['name']:
                        html += ' active'
                    html += '"><i class="far fa-circle nav-icon"></i><p>' + sub['title'] + '</p></a></li>'
                html += '</ul>'
            html += '</li>'

    return mark_safe(html)
