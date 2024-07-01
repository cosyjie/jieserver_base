from django.db import models

from .category import SET_CATEGORY


class AppsInfo(models.Model):
    icon = models.CharField(verbose_name='图标', max_length=200, null=True, blank=True)
    module_name = models.CharField(verbose_name='所属系统模块', max_length=100, default='')
    category = models.CharField(verbose_name='类别', max_length=100, choices=SET_CATEGORY)
    name_en = models.CharField(verbose_name='英文标识', max_length=100, unique=True)
    name_cn = models.CharField(verbose_name='名称', max_length=100)
    author = models.CharField(verbose_name='作者', max_length=100)
    dev_type = models.SmallIntegerField(verbose_name='组件类型', choices=((1, '官方'), (2, '第三方')))
    dependent = models.TextField(verbose_name='依赖组件', blank=True, null=True)
    version = models.CharField(verbose_name='版本', max_length=20)
    status = models.SmallIntegerField(verbose_name='状态', default=1, choices=((1, '未安装'), (2, '已安装'), (3, '已禁用')))
    description = models.TextField(verbose_name='描述', blank=True, null=True)
    download_url = models.TextField(verbose_name='下载链接', blank=True, null=True)
