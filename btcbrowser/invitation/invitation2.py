from base64 import b64encode
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re
import qrcode
import time
import os
from io import BytesIO
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def check_contain_chinese(check_str):
    for c in check_str:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False

@csrf_exempt
def generate_img(data):
    name = data['input_name']
    title = data['input_title']
    if name == '熊越':
        if title == '' or title == '院长':
            title = '院长'
        else:
            title += ' & 院长'
    elif 'Dovey' in name or '万卉' in name:
        if title == '' or title == '院花':
            title = '院花'
        else:
            title += ' & 院花'
    elif title == '':
        title = '院士'

    file_url = os.getcwd() + '/btcbrowser/invitation'

    image = Image.open(file_url + '/invitation-template-2.jpg')
    draw = ImageDraw.Draw(image)
    font_url = file_url + '/font/'
    font_url2 = os.getcwd() + '/btcbrowser/express/font/'

    if check_contain_chinese(name):
        font_name = ImageFont.truetype(font_url + 'msyhbd.ttc', 80)
    else:
        font_name = ImageFont.truetype(font_url + 'TitilliumWeb-Bold.ttf', 80)
    if check_contain_chinese(title):
        font_title = ImageFont.truetype(font_url2 + 'STHeiti.ttc', 60)
    else:
        font_title = ImageFont.truetype(font_url + 'TitilliumWeb-Regular.ttf', 60)

    color = {
        'white': '#FFFFFF',
    }

    draw.text((530, 1250), u'%s' % name, color['white'], font=font_name, spacing=10) # 加Name
    if check_contain_chinese(title):
        draw.text((530, 1400), u'%s' % title, color['white'], font=font_title, spacing=10) # 加Company
    else:
        draw.text((530, 1400), u'%s' % title, color['white'], font=font_title, spacing=10) # 加Company
    # image.show()
    return image

@csrf_exempt
def invitation2_img(request):
    data = request.POST
    if request.is_ajax():
        f = BytesIO()  # 创建一个内存地址存放图片
        image = generate_img(data)
        image.save(f, 'JPEG')  # 保存图片
        base64_data = b64encode(f.getvalue())
        s = base64_data.decode()

        return HttpResponse(s, content_type="image/jpeg")
