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

@csrf_exempt
def generate_img(data):
    file_url = os.getcwd() + '/btcbrowser/express'

    image = Image.open(file_url + '/template.png')
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font_url = file_url + '/font/'
    font = ImageFont.truetype(font_url + 'STHeiti.ttc', 55)
    font_title = ImageFont.truetype(font_url + '方正综艺简体.ttf', 70)
    font_category = ImageFont.truetype(font_url + '庞门正道标题体.ttf', 60)
    color = {
        'black': '#000000',
        'dark-grey': '#555555',
        'white': '#FFFFFF',
        'grey': '#999999',
        'bitcoin': '#f7931b',
    }
    position = {
        'title_x': 150,
        'title_y': 850,
    }


    title = data['input_title']
    # title = "比特币下一次升级要包含的Taproot究竟是什么"
    # title = "A new report indicates that Thailand's"
    category = {'1':'行业动态',}
    content = data['input_content']
    # content = '''A new report indicates that Thailand's National Legislative Assembly has endorsed an amendment to the nation's Securities and Exchange Act, allowing for the issuance of blockchain-based, tokenized securities. When the amended act becomes effective, Thailand's market should see stocks and bonds being issued and traded via blockchains.'''
    # content = '''在不久的将来，比特币用户可能会享受到一种名为“Taproot”的技术。该技术最早由比特币核心开发者兼Blockstream前CTO Gregory Maxwell提出，它将扩展比特币的智能合约灵活性，同时提供更好隐私保护。在区块链领域，即使是最复杂的智能合约，也很难跟常规区分开来。\n尽管这是一项非常大的工程，但它不仅仅是理论，是能够实现的。包括Pieter Wuille、Anthony Towns、Johnson Lau、Jonas Nick、Andrew Poelstra、Tim Ruffing、Rusty Russell以及Gregory Maxwell在内的几位最高产...'''
    # url = 'https://bitcoinmagazine.com'
    if data['input_url'] != "":
        url = data['input_url']
    else:
        url = 'https://bitcoinmagazine.com'

    def make_QR(content, sizeW = 0, sizeH = 0):#创建二维码
        qr = qrcode.QRCode(version=3, box_size=3, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image()
        if sizeW == 0 and sizeH == 0:
            return img
        w, h = img.size
        if sizeW < w or sizeH < h:
            return None
        img = img.resize((sizeW, sizeH), Image.ANTIALIAS)
        return img

    def is_english(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False

    def is_punctuation(char):
        punctuation = "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"
        # punctuation = "[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+"
        if char in punctuation:
            return True
        else:
            return False

    def CountStrLength(text):
        font = ImageFont.truetype('Arial Unicode.ttf', 22)
        strList = []
        newStr = ''
        index = 0
        for item in text:
            newStr += item
            if font.getsize(newStr)[0] > 380:
                #     print(font.getsize(newStr)[0])
                strList.append(newStr)
                newStr = ''
                # 如果后面长度不没有定长长就返回
                if font.getsize(text[index:])[0] < 415:
                    strList.append(text[index:])
                    break
            index += 1
        return strList

    def MixedContentAlign(string, length):
        str_List = []
        newStr = ""
        i = 0
        word = False
        number = False
        for s in string:
            if i < length:
                if s is '\n':
                    str_List.append(newStr)
                    newStr = ''
                    i = 0
                    continue
                if i > length - 2:
                    i += 1
                    if is_english(s):
                        str_List.append(newStr)
                        newStr = ''
                        newStr += s
                        i = 0
                        word = True
                    elif s.isdigit():
                        str_List.append(newStr)
                        newStr = ''
                        newStr += s
                        i = 0
                        number = True
                    elif is_punctuation(s):
                        newStr += s
                        if number or word:
                            i -= 1
                        else:
                            i += 0.5
                    else:
                        newStr += s
                        word = False
                        number = False
                else:
                    if is_english(s):
                        newStr += s
                        word = True
                    else:
                        if is_punctuation(s) is False:
                            if s.isdigit():
                                i += 0.5
                            else:
                                i += 1
                        else:
                            i += 0.5
                        newStr += s
                        if word:
                            i += 3.5
                            word = False
            else:
                newStr += s
                str_List.append(newStr)
                newStr = ''
                i = 0
                word = False
                number = False
        str_List.append(newStr)
        resStr = ''
        count = 0
        for item in str_List:
            resStr += item+'\n'
            count += 1
        return resStr, count

    def ContentAlign(string, x, y, font, spacing, is_title):
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zhPattern.search(string)
        if match:
            # string_list = CountStrLength(string)
            if is_title:
                resStr, count = MixedContentAlign(string, 16)
                # if len(string_list) == 0:
                #     resStr, count = MixedContentAlign(string, 16)
                # else:
                #     if len(string_list[0]) > 20:
                #         resStr, count = MixedContentAlign(string, 16)
                #     else:
                #         resStr, count = MixedContentAlign(string, len(string_list[0]))
                draw.text((x, y), resStr, color['black'], font=font, spacing=spacing)
            else:
                resStr, count = MixedContentAlign(string, 20)
                # if len(string_list) == 0:
                #     resStr, count = MixedContentAlign(string, 20)
                # else:
                #     if len(string_list[0]) > 20:
                #         resStr, count = MixedContentAlign(string, 20)
                #     else:
                #         resStr, count = MixedContentAlign(string, len(string_list[0]))
                draw.text((x, y), resStr, color['dark-grey'], font=font, spacing=spacing)
            return count
        else:
            if is_title:
                string_wrap = textwrap.fill(string, 40)
                draw.text((x, y), string_wrap, color['black'], font=font, spacing=spacing)
            else:
                string_wrap = textwrap.fill(string, 52)
                draw.text((x, y), string_wrap, color['dark-grey'], font=font, spacing=spacing)
            count = string_wrap.count('\n') + 1
            return count

    def AddTime(draw, x, y):
        # 当前时间
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        draw.text((x, y), u'%s' % cur_time, color['grey'], font)

    draw.text((position['title_x'], 750), category['1'], color['bitcoin'], font=font_category, spacing=10) # 加分类
    title_line = ContentAlign(title, position['title_x'], position['title_y'], font_title, spacing=20, is_title=True) # 加标题
    time_y = position['title_y'] + 100 * title_line
    addtime = AddTime(draw, position['title_x'], time_y) # 加时间
    content_line = ContentAlign(content, position['title_x'], time_y + 100, font, spacing=25, is_title=False) # 加正文
    # image.paste(logo, (-20, 150), mask=a) # 加logo
    QR_res = make_QR(url, 400, 400)  # 创建二维码
    image.paste(QR_res, (int((width-400)/2), height-650)) # 加二维码
    # image.save(file_url + '/output.png') # 导出图片
    return image

@csrf_exempt
def express_img(request):
    data = request.POST
    if request.is_ajax():
        f = BytesIO() # 创建一个内存地址存放图片
        image = generate_img(data)
        image.save(f, 'PNG')  # 保存图片
        base64_data = b64encode(f.getvalue())
        s = base64_data.decode()
        return HttpResponse(s)
