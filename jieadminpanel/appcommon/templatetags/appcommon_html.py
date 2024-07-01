from django import template

from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag
def form_btn(*args, **kwargs):
    html = ''
    if 'submit' in args:
        html += ' <button type="submit" lay-submit class="btn btn-info margin_right_5" id="form_btn_submit" name="form_btn_submit">提交</button>'
    if 'submit_by_txt' in args:
        btn_txt = kwargs['btn_txt']
        html += f' <button type="submit" lay-submit class="btn btn-info margin_right_5" id="form_btn_submit" name="form_btn_submit">{btn_txt}</button>'
    if 'back' in args:
        html += ' <button type="button" lay-reset class="btn btn-default float-right margin_right_5" id="form_btn_back" ' \
                'name="form_btn_back" onclick="javascript:history.back();">返回</button> '
    if 'reset' in args:
        html += ' <button type="reset" class="btn btn-secondary float-right margin_right_5" id="form_btn_reset" ' \
                'name="form_btn_reset">重置</button> '
    if 'search' in args:
        html += ' <button type="button" class="btn btn-primary margin_right_5" id="search_form_btn_search">' \
                '<i class="fa fa-search"></i> 查询</button>'

    return mark_safe(html)