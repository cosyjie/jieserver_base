from django import forms
from appcommon.forms import FormBase


class HostnameForm(FormBase):
    """ 修改当前主机名表单 """
    error_messages = {'required': '必须要指定主机名称！'},
    hostname = forms.CharField(label="主机名", widget=forms.TextInput(
        attrs={'class': 'layui-input ', 'lay-verify': 'required', 'lay-reqtext': '请输入主机名！'}
    ))


class TimezoneForm(FormBase):
    """时区表单"""
    zone = forms.CharField(label='时区')
    time_sync = forms.IntegerField()
    set_date = forms.CharField()