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
    company = data['input_company']

    file_url = os.getcwd() + '/btcbrowser/invitation'

    image = Image.open(file_url + '/invitation-template.jpg')
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font_url = file_url + '/font/'
    font_url2 = os.getcwd() + '/btcbrowser/express/font/'

    if check_contain_chinese(name):
        font_name = ImageFont.truetype(font_url + 'msyhbd.ttc', 120)
    else:
        font_name = ImageFont.truetype(font_url + 'TitilliumWeb-Bold.ttf', 120)
    if check_contain_chinese(company):
        font_company = ImageFont.truetype(font_url2 + 'STHeiti.ttc', 90)
    else:
        font_company = ImageFont.truetype(font_url + 'TitilliumWeb-Regular.ttf', 90)

    color = {
        'white': '#FFFFFF',
    }
    position = {
        'middle': width/2,
    }

    w1, h1 = font_name.getsize(name)
    w2, h2 = font_company.getsize(company)

    draw.text((position['middle'] - w1/2, 750), u'%s' % name, color['white'], font=font_name, spacing=10) # 加Name
    if check_contain_chinese(company):
        draw.text((position['middle'] - w2/2, 950), u'%s' % company, color['white'], font=font_company, spacing=10) # 加Company
    else:
        draw.text((position['middle'] - w2/2, 920), u'%s' % company, color['white'], font=font_company, spacing=10) # 加Company
    # image.show()
    return image

@csrf_exempt
def invitation_img(request):
    data = request.POST
    if request.is_ajax():
        f = BytesIO()  # 创建一个内存地址存放图片
        image = generate_img(data)
        image.save(f, 'JPEG')  # 保存图片
        base64_data = b64encode(f.getvalue())
        s = base64_data.decode()

        return HttpResponse(s, content_type="image/jpeg")
