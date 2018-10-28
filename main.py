# -*- coding: UTF-8 -*-
import sys
import time
import leveldb
from urllib import quote_plus
import re
import json
import itertools
import sys
import requests
from Queue import Queue
from threading import Thread


def getCoupons(itemNumId):
    exParams = {
        "spm": "a230r.1.14.8.22fc51barOCtpH",
        "id": itemNumId,
        "ns": "1",
        "abbucket": "7"
    }
    data = {
        "itemNumId": itemNumId,
        "exParams": json.dumps(exParams),
        "detail_v": "3.1.1",
        "ttid": "2018@taobao_iphone_9.9.9",
        "utdid": "123123123123123"
    }

    data_part = quote_plus(json.dumps(data))
    url = ('https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + data_part).replace('+', '')
    header = {}
    response = requests.get(url, timeout=5, headers=header).json()

    print response['data']
    api = json.loads(response['data']['apiStack'][0]['value'])
    if api['feature'].has_key('hasCoupon') and api['feature']['hasCoupon'] == 'true':
        coupons_origin = api['resource']['coupon']['couponList']
        key = 'title'
    elif api['price'].has_key('shopProm'):
        coupons_origin = api['price']['shopProm'][0]['content']
        key = 'content'
    else:
        coupons_origin = []

    coupons = []
    if len(coupons_origin) == 0: return (coupons)

    for coupon_origin in coupons_origin:
        if key == 'title':
            content = coupon_origin[key]
        else:
            content = coupon_origin

        for sub_coupon in content.split(';'):
            if '领津贴' in sub_coupon: continue

            matchObj = re.match(".*满(\d+)(.{3}).*[减省](\d+).*", sub_coupon.encode('utf-8'))

            if matchObj:
                condition = matchObj.group(1)
                unit = matchObj.group(2)
                discount = matchObj.group(3)
                coupon = {
                    "condition": condition,
                    "unit": unit,
                    "discount": discount
                }
                coupons.append(coupon)

    return (coupons)

def url_get(url):
    # print('GET ' + url)
    header = dict()
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header['Accept-Encoding'] = 'gzip,deflate,sdch'
    header['Accept-Language'] = 'en-US,en;q=0.8'
    header['Connection'] = 'keep-alive'
    header['DNT'] = '1'
    # header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
    header['User-Agent'] = 'Mozilla/12.0 (compatible; MSIE 8.0; Windows NT)'
    return requests.get(url, timeout=5, headers=header).text

def getSearchResult(itemName):
    URL_BASE = 'http://s.m.taobao.com/search?q={}&n=200&m=api4h5&style=list&page={}'
    item_page = '1'
    url = URL_BASE.format(quote_plus(item_name), item_page)

    search = []
    for tr in range(5):
        try:
            items_obj = json.loads(url_get(url))
            break
        except KeyboardInterrupt:
            quit()
        except Exception as e:
            if tr == 4: raise e

    if len(items_obj['listItem']) == 0:
        print('no listItem')

    for item in items_obj['listItem']:
        itemNumId = item['itemNumId']
        coupons = getCoupons(item['itemNumId'])
        if len(coupons) > 0:
            hasCoupon = True
        else:
            hasCoupon = False
        item_obj = dict(
            itemNumId=int(item['itemNumId']),
            userId=item['userId'],
            name=item['name'],
            nick=item['nick'],
            price=float(item['price']),
            coupons=coupons,
            hasCoupon=hasCoupon
        )
        search.append(item_obj)
    return(search)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    item_names = ['壹可医研杏仁酸','壹可医研弹力美肌水']
    for item_name in item_names:
        search = getSearchResult(item_name)
        for s in search:
            print s['userId']

