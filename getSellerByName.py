# -*- coding: UTF-8 -*-
from urllib import quote_plus
import urllib2
import sys
from lxml import etree


def getSellerByName(seller):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    URL_BASE = 'https://shop.m.taobao.com/shop/shop_search.htm?q={}'
    url = URL_BASE.format(quote_plus(seller))

    header = {}
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)
    html = response.read().decode('utf-8')

    tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
    tables = tree.xpath('//div[@class="detail"]/table')

    if len(tables) == 0: return 0

    res = dict()
    for i, table in enumerate(tables):
        if i == 0: continue
        img = table.xpath('//tr/td[@class="pic"]/a/img')[0].attrib
        products = table.xpath('./tr/td[@valign="middle"]/a/text()')[0]
        res[i] = {
            "icon_url": img.get('src'),
            "name": img.get('alt'),
            "products": products
        }
    return(res)



if __name__ == '__main__':
    #seller = 'ECOONER旗舰店'
    seller = 'ECOONER'
    print getSellerByName(seller)