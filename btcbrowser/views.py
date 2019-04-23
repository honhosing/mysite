from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
import time

# Create your views here.
def ErrorResponse(message):
    data = {}
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)

def timestamp_datatime(value):
    # format = '%Y-%m-%d %H:%M'
    format = '%Y-%m-%d %H:%M:%S'
    #value 为时间戳值,如:1460073600.0
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

def cal_diff(num):
    level = int(len(str(int(num))) / 3)
    cal_level = {
        0: 1, 1: 10 ** 3, 2: 10 ** 6, 3: 10 ** 9, 4: 10 ** 12
    }
    unit = {
        0: 'B', 1: 'K', 2: 'M', 3: 'G', 4: 'T'
    }
    result = str(round(int(num) / cal_level[level], 2)) + ' ' + unit[level]
    return result

def get_data_by_height(text):
    url = 'https://chain.api.btc.com/v3/block/{}'.format(text)
    get_data = json.loads(requests.get(url).text)
    data = {}
    data['height'] = get_data.get('data').get('height')
    data['prev_height'] = data['height'] - 1
    data['next_height'] = data['height'] + 1
    data['confirmations'] = get_data.get('data').get('confirmations')
    data['reward_block'] = get_data.get('data').get('reward_block') / 10**8
    data['reward_fees'] = get_data.get('data').get('reward_fees') / 10**8
    if get_data.get('data').get('is_sw_block'):
        data['is_sw_block'] = '已采用'
    else:
        data['is_sw_block'] = '未采用'
    data['size'] = get_data.get('data').get('size')
    data['weight'] = get_data.get('data').get('weight')
    data['tx_count'] = get_data.get('data').get('tx_count')
    data['version'] = get_data.get('data').get('version')

    data['difficulty'] = cal_diff(get_data.get('data').get('difficulty'))
    data['pool_difficulty'] = cal_diff(get_data.get('data').get('pool_difficulty'))
    data['bits'] = get_data.get('data').get('bits')
    data['nonce'] = get_data.get('data').get('nonce')
    data['pool_link'] = get_data.get('data').get('extras').get('pool_link')
    data['pool_name'] = get_data.get('data').get('extras').get('pool_name')
    data['timestamp'] = timestamp_datatime(get_data.get('data').get('timestamp'))
    data['hash'] = get_data.get('data').get('hash')
    if get_data.get('data').get('prev_block_hash') == '0000000000000000000000000000000000000000000000000000000000000000':
        data['prev_block_hash'] = '不存在'
    else:
        data['prev_block_hash'] = get_data.get('data').get('prev_block_hash')
    if get_data.get('data').get('next_block_hash') == '0000000000000000000000000000000000000000000000000000000000000000':
        data['next_block_hash'] = '还没出块'
    else:
        data['next_block_hash'] = get_data.get('data').get('next_block_hash')
    data['mrkl_root'] = get_data.get('data').get('mrkl_root')
    return data

def get_data_by_address(hash):
    url = 'https://chain.api.btc.com/v3/address/{}'.format(hash)
    get_data = json.loads(requests.get(url).text)
    data = {}
    data['address'] = get_data.get('data').get('address')
    data['balance'] = get_data.get('data').get('balance') / 10**8
    data['received'] = get_data.get('data').get('received') / 10**8
    data['sent'] = get_data.get('data').get('sent') / 10**8
    data['tx_count'] = get_data.get('data').get('tx_count')
    data['unconfirmed_tx_count'] = get_data.get('data').get('unconfirmed_tx_count')
    return data


def get_data_by_txhash(hash):
    url = 'https://chain.api.btc.com/v3/tx/{}?verbose=3'.format(hash)
    get_data = json.loads(requests.get(url).text)
    data = {}
    data['block_height'] = get_data.get('data').get('block_height')
    data['confirmations'] = get_data.get('data').get('confirmations')
    data['block_time'] = timestamp_datatime(get_data.get('data').get('block_time'))
    data['size'] = get_data.get('data').get('size')
    data['vsize'] = get_data.get('data').get('vsize')
    data['weight'] = get_data.get('data').get('weight')
    data['inputs_value'] = get_data.get('data').get('inputs_value') / 10**8
    data['outputs_value'] = get_data.get('data').get('outputs_value') / 10 ** 8
    data['sigops'] = get_data.get('data').get('sigops')
    data['fee'] = get_data.get('data').get('fee') / 10 ** 8
    data['weight'] = get_data.get('data').get('weight')
    data['weight'] = get_data.get('data').get('weight')
    return data


def get_blockchain_data(request):
    string = request.GET.get("search")
    if string is None:
        context = {}
        context['status'] = 'EMPTY'
        return context
    else:
        try:
            if string == 'latest' or string == '0' or (len(string) < 8 and type(eval(string)) == int):
                context = get_data_by_height(string)
                context['status'] = 'SUCCESS'
                context['type'] = 'height'
                context['title'] = '【高度】：' + string
            elif len(string) == 34:
                context = get_data_by_address(string)
                context['status'] = 'SUCCESS'
                context['type'] = 'address'
                context['title'] = '【地址】：' + string
            elif len(string) == 64:
                context = get_data_by_txhash(string)
                context['status'] = 'SUCCESS'
                context['type'] = 'transaction'
                context['title'] = '【交易哈希】：' + string
            else:
                context = {}
                context['status'] = 'ERROR'
                context['title'] = string
            return context
        except:
            context = {}
            context['status'] = 'ERROR'
            context['title'] = string
            return context

def btcbrowser(request):
    context = get_blockchain_data(request)
    return render(request, 'btcbrowser.html', context)

    # '''
    # string_of_address = '15urYnyeJe3gwbGJ74wcX89Tz7ZtsFDVew'  # 34位数
    # string_of_tx = '0eab89a271380b09987bcee5258fca91f28df4dadcedf892658b9bc261050d96' # 64位数
    #
    # 按区块高度取区块状态数据，如，取最新块及高度为3的块：url = 'https://chain.api.btc.com/v3/block/latest,3'
    # 获取某一天出的区块的数据列表，按照倒序排列。GET /block/date/{ymd}，如：url = 'https://chain.api.btc.com/v3/block/date/20151215'
    # 根据区块高度获取区块交易列表。GET /block/{xxx}/tx，如：url='https://chain.api.btc.com/v3/block/latest/tx'
    # 根据交易哈希值获取交易详情。GET /tx/{txhash}，如：
    #  - 获取单个交易的全部信息
    #  --- https://chain.api.btc.com/v3/tx/0eab89a271380b09987bcee5258fca91f28df4dadcedf892658b9bc261050d96?verbose=3
    #  - 获取多个交易
    #  --- https://chain.api.btc.com/v3/tx/000000000000000005cb6f6e2f09e84a353ab91756a38aa50fbaf25059f76666,0ba9252660a6a5f291a8983092074f9a1da5f6d1c790518d6550f054e60bbab1
    # 获取未确认交易的哈希。GET /tx/unconfirmed，如：url='https://chain.api.btc.com/v3/tx/unconfirmed'
    # 获取未确认交易的信息，包括体积和数量。GET /tx/unconfirmed/summary，如：url='https://chain.api.btc.com/v3/tx/unconfirmed/summary'
    # 获取地址的信息。GET /address/{address}，如：url='https://chain.api.btc.com/v3/address/15urYnyeJe3gwbGJ74wcX89Tz7ZtsFDVew,1PErRgFdo757pyyMxFiwB326vuymXC3hev'
    # 获取地址的交易列表，按照倒序排列。GET /address/{address}/tx，
    #  - 参数：
    #  --- page，可选，默认为1，页码
    #  --- pagesize，可选，默认为50，可选范围为1-50，分页大小
    # 如：url='https://chain.api.btc.com/v3/address/15urYnyeJe3gwbGJ74wcX89Tz7ZtsFDVew/tx'
    # 获取地址的未花费交易列表，按照确认数正序排列。GET /address/{address}/unspent，如：url='https://chain.api.btc.com/v3/address/15urYnyeJe3gwbGJ74wcX89Tz7ZtsFDVew/unspent'
    # '''


def test(request):
    return render(request, 'test.html')

def express(request):
    return render(request, 'express.html')

def halving(request):
    context = {}
    timestamp_now = int(time.time())
    btc_timestamp_tar = 1590332601
    ltc_timestamp_tar = 1565126670
    context['btc_time_leave'] = btc_timestamp_tar - timestamp_now
    context['ltc_time_leave'] = ltc_timestamp_tar - timestamp_now
    return render(request, 'halving.html', context)

def bitcoin_orange(request):
    return render(request, 'bitcoin-orange.html')

def qgkd(request):
    return render(request, '7gkd/index.html')
