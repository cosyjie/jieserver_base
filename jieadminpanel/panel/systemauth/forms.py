from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class LoginForm(AuthenticationForm):
    """登录表单"""
    username = UsernameField(
        error_messages={'required': '请输入登录用户名！'},
        widget=forms.TextInput(
            attrs={
                'autofocus': True, 'class': 'layui-input', 'lay-verify': 'required', 'placeholder': '用户名',
                'lay-reqtext': '请输入用户名！', 'autocomplete': 'off', 'lay-affix': 'clear'
            }
        )
    )
    password = forms.CharField(
        error_messages={'required': '请输入登录密码！'},
        widget=forms.PasswordInput(attrs={
            'lay-verify': 'required', 'placeholder': '密码', 'lay-reqtext': '请输入密码！', 'autocomplete': 'off',
            'class': 'layui-input', 'lay-affix': 'yes'
        }
        ),
    )