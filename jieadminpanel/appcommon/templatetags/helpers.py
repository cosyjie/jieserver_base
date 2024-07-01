import socket
from importlib import import_module
from django import template
from django.urls import reverse
from django.conf import settings
from django.utils.html import format_html, mark_safe


register = template.Library()


@register.simple_tag
def menu(parent_menu, submenu):
    menus = {}
    html = ''
    for app in settings.INSTALLED_APPS:
        if app[:5] == 'apps.':
            append_list = import_module(app + '.menu')
            menu_list = append_list.menu
            for k, v in menu_list.items():
                if k in menus:
                    if v['child']:
                        for child in v['child']:
                            if child not in menus[k]['child']:
                                menus[k]['child'].append(child)
                else:
                    menus[k] = v

    for k, value in menus.items():
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
                if parent_menu == k and submenu == sub['name']:
                    html += ' active'
                html += '"><i class="far fa-circle nav-icon"></i><p>' + sub['title'] +'</p></a></li>'
            html += '</ul>'
        html += '</li>'

    return mark_safe(html)