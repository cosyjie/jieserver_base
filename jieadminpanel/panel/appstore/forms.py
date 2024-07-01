from django import forms
from appcommon.forms import FormBase


class DeleteConfirmForm(FormBase):
    name_confirm = forms.CharField(
        label='请输入要删除的组件名称以确认删除!',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )