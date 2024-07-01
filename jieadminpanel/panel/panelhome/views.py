import subprocess
import platform
import psutil
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import FormView

from appcommon.helper import subprocess_run
from panel.panelhome.forms import HostnameForm, TimezoneForm


class HomeMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_menu'] = 'home'
        return context


def get_system_info():
    context = {}
    context['current_time'] = subprocess.run('date +"%F %T %Z"', shell=True, capture_output=True,
                                             encoding='utf-8').stdout.strip()
    context['cpu_count'] = psutil.cpu_count()
    context['cpu'] = "{}, {} 核".format(
        subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, encoding="utf-8") \
            .stdout.split('\t')[6].lstrip(': ').rstrip('stepping'), context['cpu_count'])
    context['cpu_percent'] = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    context['mem_percent'] = mem.percent
    context['mem'] = '({}%){}GB/{}GB '.format(
        context['mem_percent'], round(mem.used / 1024 / 1024 / 1024, 2), round(mem.total / 1024 / 1024 / 1024, 2)
    )
    swap_memory = psutil.swap_memory()
    context['swap_percent'] = swap_memory.percent
    context['swap'] = '({}%){}GB/{}GB'.format(
        context['swap_percent'], round(swap_memory.used / 1024 / 1024 / 1024, 2),
        round(swap_memory.total / 1024 / 1024 / 1024, 2)
    )

    sysusage = psutil.disk_usage('/')
    context['sysdisk_percent'] = round(sysusage.percent, 2)
    context['sysdisk'] = '({}%){}GB/{}GB '.format(
        sysusage.percent, round(sysusage.used / 1024 / 1024 / 1024, 2),
        round(sysusage.total / 1024 / 1024 / 1024, 2)
    )

    homeusage = psutil.disk_usage('/home')
    context['homedisk_percent'] = round(homeusage.percent, 2)
    context['homedisk'] = '({}%){}GB/{}GB '.format(
        homeusage.percent, round(homeusage.used / 1024 / 1024 / 1024, 2),
        round(homeusage.total / 1024 / 1024 / 1024, 2)
    )

    rootusage = psutil.disk_usage('/root')
    context['rootdisk_percent'] = round(rootusage.percent, 2)
    context['rootdisk'] = '({}%){}GB/{}GB  '.format(
        rootusage.percent, round(rootusage.used / 1024 / 1024 / 1024, 2),
        round(rootusage.total / 1024 / 1024 / 1024, 2)
    )

    os_getloadavg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    context['os_avg_percent'] = round(os_getloadavg[0],2)
    get_percent = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    context['os_getloadavg'] = '1分钟: {}%, 5分钟: {}%, 15分钟:{}%'.format(
        round(get_percent[0], 2),  round(get_percent[1], 2), round(get_percent[2], 2)
    )
    context['version'] = settings.VERSION
    return context


class SystemHomeView(HomeMixin, TemplateView):
    template_name = 'panelhome/home.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['page_title'] = '概览'
        context['hostname'] = subprocess_run(subprocess, 'hostname').stdout.strip("\n")
        context['os'] = subprocess_run(subprocess, 'cat /etc/redhat-release').stdout.strip()
        context['platform'] = "{} 运行于 {}".format(platform.platform(), platform.machine())

        context.update(get_system_info())
        return context


def system_state_view(request):
    return JsonResponse(get_system_info())


class HostnameView(HomeMixin, FormView):
    form_class = HostnameForm
    template_name = 'panelhome/hostname.html'
    success_url = reverse_lazy('panelhome:hostname')

    def get_initial(self):
        self.initial['hostname'] = subprocess_run(subprocess,'hostname').stdout.strip("\n")
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '配置主机名'
        context['breadcrumb'] = [
            {'title': '概览', 'href': reverse_lazy('panelhome:index'), 'active': False},
            {'title': '配置主机名', 'href': '', 'active': True},
        ]
        return context

    def form_valid(self, form):
        hostname = form.cleaned_data['hostname']
        run_end = subprocess_run(subprocess,'hostnamectl set-hostname ' + hostname)
        if run_end.returncode == 0:
            messages.success(self.request, '修改主机名成功！')
        else:
            messages.warning(self.request, '<p>修改失败！主机执行信息：</p>{}'.format(run_end.stderr))

        return super().form_valid(form)


class TimezoneView(HomeMixin, FormView):
    template_name = 'panelhome/timezone.html'
    form_class = TimezoneForm
    success_url = reverse_lazy('panelhome:timezone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '时区和时间'
        context['breadcrumb'] = [
            {'title': '仪表板', 'href': reverse_lazy('panelhome:index'), 'active': False},
            {'title': '配置时区和时间', 'href': '', 'active': True},
        ]
        run_end = subprocess_run(subprocess, 'timedatectl')
        if run_end.returncode == 0:
            context['current_zone'] = run_end.stdout.strip().split('\n')[3].split(':')[1].strip()
        cmd = 'timedatectl list-timezones'
        context['zone_list'] = subprocess_run(subprocess, cmd).stdout.strip().split('\n')
        context['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmd = "timedatectl | grep 'NTP service'"
        context['time_sync'] = subprocess_run(subprocess, cmd).stdout.replace('NTP service: ', '').strip()
        return context

    def form_valid(self, form):
        zone = form.cleaned_data.get('zone')
        time_sync = form.cleaned_data.get('time_sync')
        cmd = 'timedatectl set-timezone {}'.format(zone)
        run_end = subprocess_run(subprocess, cmd)
        if run_end.returncode != 0:
            messages.warning(self.request, '设置时区异常，服务器执行信息：' + run_end.stderr)
        else:
            messages.success(self.request, '设置时区操作成功！')
            if time_sync == 1:
                run_end = subprocess_run(subprocess, 'timedatectl set-ntp yes')
                if run_end.returncode != 0:
                    messages.warning(self.request, '启用同步异常，服务器执行信息：' + run_end.stderr)
                else:
                    messages.success(self.request, '启用自动网络同步操作完成！')
            if time_sync == 2:
                run_end = subprocess_run(subprocess, 'timedatectl set-ntp no')
                if run_end.returncode == 0:
                    set_date = form.cleaned_data.get('set_date')
                    run_end = subprocess_run(subprocess, 'date -s "{}"'.format(set_date))
                    if run_end.returncode != 0:
                        messages.warning(self.request, '设置日期异常，服务器执行信息：' + run_end.stderr)
                    else:
                        messages.success(self.request, '设置手动日期完成!')
                else:
                    messages.warning(self.request, '停用同步异常，服务器执行信息：' + run_end.stderr)

        return super().form_valid(form)


