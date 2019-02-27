from urllib.parse import urlencode
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_login_qq_url():
    params = {
        'response_type': 'code',
        'client_id': settings.QQ_APP_ID, # 开发者的appid
        'redirect_uri': settings.QQ_REDIRECT_URL, # 网站应用的回调域
        'state': settings.QQ_STATE,
    }
    return 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)
