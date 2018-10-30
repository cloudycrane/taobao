# -*- coding: UTF-8 -*-
from urllib import quote_plus
import urllib2
import sys
import json

def url_get(url):
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Language':'zh-CN,zh;q=0.3',
        'Referer':'https://item.taobao.com/item.htm',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Connection':'keep-alive',
    }
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    return response.read().decode('utf-8')

def getItemBySeller(shopId):
    item_page = '1'
    result = dict()
    i = 1
    while True:
        URL_BASE = 'http://api.s.m.taobao.com/search.json?m=shopitemsearch&shopId={}&n=40&page={}'
        url = URL_BASE.format(quote_plus(shopId), item_page)
        for tr in range(5):
            try:
                items_obj = json.loads(url_get(url))
                break
            except KeyboardInterrupt:
                quit()
            except Exception as e:
                if tr == 4: raise e

        if len(items_obj['itemsArray']) == 0:
            print('no listItem')
            break

        for item in items_obj['itemsArray']:
            result[i] = {
                'id': item['item_id'],
                'title': item['title'],
                'price': item['price'],
                'priceWithRate': item['priceWithRate'],
                'isprepay': int(item['isprepay']) if item.has_key('isprepay') else 0,
                'type': item['type'],
                'sold': item['sold'],
                'quantity': item['quantity'],
                'pic_path': item['pic_path']
            }
            i += 1

        if int(items_obj['totalPage']) > int(item_page):
            item_page = str(int(item_page) + 1)
        else:
            break

    return(result)



if __name__ == '__main__':
    shopId = '192173170'
    print getItemBySeller(shopId)